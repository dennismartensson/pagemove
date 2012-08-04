from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'serverChromeToIpad.views.home', name='home'),
    # url(r'^serverChromeToIpad/', include('serverChromeToIpad.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'urlShare.views.index', name='index'),
    url(r'^saveUrl/$', 'urlShare.views.saveUrl', name='saveUrl'),
    url(r'^saveUrlFast/$', 'urlShare.views.saveUrlFast', name='saveUrlFast'),
    url(r'^validToken/$', 'urlShare.views.validToken', name='validToken'),
    url(r'^bookmarklet/$', 'urlShare.views.bookmarklet', name='bookmarklet'),
    url(r'^getLastPage/$', 'urlShare.views.getLastPage', name='getLastPage'),
    url(r'^getHistory/$', 'urlShare.views.getHistory', name='getHistory'),
    (r'^$', include('twython_django_oauth.urls')),
    url(r'^login/?$', "urlShare.views.begin_auth", name="twitter_login"),
    url(r'^thanks/?$', "urlShare.views.thanks", name="twitter_callback"),
    url(r'^regisert_device/?$', "urlShare.views.regisert_device", name="regisert_device"),
    url(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/static/img/favicon.ico'}),
    url(r'^shakeSend/$', 'urlShare.views.shakeSend', name='shakeSend'),
    url(r'^webapp/$', 'urlShare.views.webapp', name='webapp'),
    
)
