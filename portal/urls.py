from django.conf.urls import patterns, include, url
from portal.views import *
from RushAKPsi import settings
from django.conf.urls.static import static

urlpatterns = patterns('',

    url(r'^$', index_view),

    url(r'application/', application_view),

    url(r'login/', login_view),

    url(r'signup/', signup_view),

    url(r'gallery/', gallery_view),

    url(r'logout/', logout_view), 

    url(r'rushee/(?P<rushee_id>\d+)/', rushee_view),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

