from django.conf import urls

from .views import download, download_list

urlpatterns = [
    urls.url(r'^$', download_list),
    urls.url(r'(?P<download_id>\d+)/$', download, name='download'),
]
