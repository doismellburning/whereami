from datetime import datetime
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import mail_admins
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
import logging
from main.models import *
import urllib2

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

@login_required
def whereami(request):
    user_id = int(request.GET.get('user', settings.FOURSQUARE_USER_ID))

    checkin = LatestCheckin.objects.get(user_id=user_id).checkin
    visitor = request.user.email
    visit_at = datetime.now()

    Visit.objects.create(username=visitor, when=visit_at, checkin=checkin)

    mail_admins("Where Are You? by %s" % visitor, "%s saw you were at %s at %s" % (visitor, checkin.venue['name'], visit_at))

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

@login_required
def home(request):
    return render(request, 'map.html')

def foursquare_oauth(request):
    url = 'https://foursquare.com/oauth2/authenticate?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}'.format(client_id=settings.FOURSQUARE_CLIENT_ID, redirect_uri=settings.FOURSQUARE_CALLBACK_URL)
    mail_admins('Auth', url)
    return HttpResponseRedirect(url)

def foursquare_callback(request):
    code = request.GET.get('code')
    url = "https://foursquare.com/oauth2/access_token?client_id={client_id}&client_secret={client_secret}&grant_type=authorization_code&redirect_uri={redirect_uri}&code={code}".format(client_id=settings.FOURSQUARE_CLIENT_ID, client_secret=settings.FOURSQUARE_CLIENT_SECRET, redirect_uri=settings.FOURSQUARE_CALLBACK_URL, code=code)
    mail_admins('Callback', url)

    #Optimism, but this is a one-off process just for me, saving me doing a manual curl
    f = urllib2.urlopen(url)
    response = f.read()
    j = json.loads(response)
    access_token = j['access_token']
    #Consider saving? But don't really care - just want push

    logger.info(access_token)
    return HttpResponseRedirect(reverse('home'))
