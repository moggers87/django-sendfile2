from django.conf import urls

from .views import direct_download, download, download_list

urlpatterns = [
    urls.url(r'(?P<download_id>\d+)/$', download, name='download'),
    urls.url(r'^$', download_list),
    urls.url(r'direct/(?P<filename>.*)$', direct_download, name='direct_download'),
]
