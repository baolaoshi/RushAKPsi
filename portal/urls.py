from django.conf.urls import patterns, include, url
from portal.views import *

urlpatterns = patterns('',

    url(r'^$', index_view),

    url(r'application/', application_view),

    url(r'login/', login_view),

    url(r'signup/', signup_view),

    url(r'gallery/', gallery_view),
)
