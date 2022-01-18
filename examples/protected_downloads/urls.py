from django import urls
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    urls.re_path(r'^', urls.include('download.urls')),
    urls.re_path(r'^admin/', admin.site.urls),
]
