from django.conf.urls import url
from django.contrib import admin

from core.views import get_dict

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^dict/', get_dict),
]
