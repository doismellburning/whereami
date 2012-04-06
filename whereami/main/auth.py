from django.contrib.auth.models import User
from openid.consumer.consumer import SUCCESS
from django.core.mail import mail_admins
import hashlib

class GoogleBackend:

    def authenticate(self, openid_response):
        if openid_response is None:
            return None
        if openid_response.status != SUCCESS:
            return None

        google_email = openid_response.getSigned('http://openid.net/srv/ax/1.0', 'value.email')
        google_firstname = openid_response.getSigned('http://openid.net/srv/ax/1.0', 'value.firstname')
        google_lastname = openid_response.getSigned('http://openid.net/srv/ax/1.0', 'value.lastname')

        # Sigh 30 char limit on username :( - I realise md5 generally bad, but not convinced I need to care for this usage
        username = hashlib.md5(google_email).hexdigest()[:30]
        (user, _) = User.objects.get_or_create(email=google_email, username=username)

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
