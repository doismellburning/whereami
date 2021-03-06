from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView

urlpatterns = patterns('main.views',
    url(r'^$', 'home', name='home'),
    url(r'^favicon.ico$', RedirectView.as_view(url='http://example.com/favicon.ico', permanent=False)),
    url(r'^foursquare/push/', 'foursquare_push'),
    url(r'^whereami/$', 'whereami', name='whereami'),
    url(r'^foursquare/oauth/$', 'foursquare_oauth'),
    url(r'^foursquare/callback/$', 'foursquare_callback'),
    # Examples:
    # url(r'^$', 'whereami.views.home', name='home'),
    # url(r'^whereami/', include('whereami.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    url(r'^login/$', 'django_openid_auth.views.login_begin', name='openid-login'),
    url(r'^login-complete/$', 'django_openid_auth.views.login_complete', name='openid-complete'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/',}, name='logout'),
)
