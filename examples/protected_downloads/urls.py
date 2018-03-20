from django.conf import urls

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    urls.url(r'^', urls.include('download.urls')),
    urls.url(r'^admin/', urls.include(admin.site.urls)),
]
