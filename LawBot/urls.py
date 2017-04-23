from django.conf.urls import url
from django.contrib import admin

from core.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^dict/', get_dict),
    url(r'^email/(?P<email>[\s\S]+)/$', send_email),
]

