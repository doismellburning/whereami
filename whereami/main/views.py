from django.conf import settings
from django.core.mail import mail_admins
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
import json
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def foursquare_push(request):
    secret = request.POST['secret']
    if secret != settings.FOURSQUARE_PUSH_SECRET:
         logger.warn('Pushed secret ({secret}) did not match secret'.format(secret=secret))
         return HttpResponseForbidden('Invalid secret')

    checkin = request.POST['checkin']
    checkin = json.loads(checkin)

    mail_admins('Checkin', json.dumps(checkin, indent=4))

    return HttpResponse()
