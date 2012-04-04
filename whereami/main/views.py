from django.conf import settings
from django.core.mail import mail_admins
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
import json
import logging
from main.models import *

logger = logging.getLogger(__name__)

@csrf_exempt
def foursquare_push(request):
    secret = request.POST['secret']
    if secret != settings.FOURSQUARE_PUSH_SECRET:
         logger.warn('Pushed secret ({secret}) did not match secret'.format(secret=secret))
         return HttpResponseForbidden('Invalid secret')

    checkin_str = request.POST['checkin']
    checkin_dict = json.loads(checkin_str)
    # mail_admins('Checkin', json.dumps(checkin_dict, indent=4))
    checkin = Checkin(**checkin_dict)
    checkin.save()

    user_id = int(checkin.user["id"])

    (latest_checkin, _) = LatestCheckin.objects.get_or_create(user_id=user_id)
    latest_checkin.checkin = checkin
    latest_checkin.save()

    return HttpResponse()

def whereami(request):
    user_id = int(request.GET.get('user', settings.FOURSQUARE_USER_ID))

    checkin = LatestCheckin.objects.get(user_id=user_id).checkin

    return HttpResponse(json.dumps(checkin, default=_json_encode))

def _json_encode(obj):
    from bson import ObjectId
    from mongoengine import Document, EmbeddedDocument

    if isinstance(obj, (Document, EmbeddedDocument)):
        out = dict(obj._data)
        for k,v in out.items():
            if isinstance(v, ObjectId):
                out[k] = str(v)
    else:
        raise TypeError, "Could not JSON-encode type '%s': %s" % (type(obj),
str(obj))
    return out

