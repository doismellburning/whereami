from django.conf.urls import patterns, include, url

urlpatterns = patterns('main.views',
    url(r'^foursquare/push/', 'foursquare_push'),
    url(r'^whereami/$', 'whereami'),
    # Examples:
    # url(r'^$', 'whereami.views.home', name='home'),
    # url(r'^whereami/', include('whereami.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
