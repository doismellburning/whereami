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
