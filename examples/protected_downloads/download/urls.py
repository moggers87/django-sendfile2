from django import urls

from .views import direct_download, download, download_list

urlpatterns = [
    urls.re_path(r'(?P<download_id>\d+)/$', download, name='download'),
    urls.re_path(r'^$', download_list),
    urls.re_path(r'direct/(?P<filename>.*)$', direct_download, name='direct_download'),
]
