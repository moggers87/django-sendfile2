from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.urls import reverse

sendfile_storage = FileSystemStorage(location=settings.SENDFILE_ROOT)


class Download(models.Model):
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    is_public = models.BooleanField(default=True)
    title = models.CharField(max_length=255)
    # files stored in SENDFILE_ROOT directory (which should be protected)
    file = models.FileField(upload_to='download', storage=sendfile_storage)

    def is_user_allowed(self, user):
        return self.users.filter(pk=user.pk).exists()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('download', kwargs={"download_id": self.pk})

    class Meta:
        app_label = "download"
