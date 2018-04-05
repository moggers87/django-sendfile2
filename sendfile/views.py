from django.views.generic.detail import BaseDetailView
from sendfile import sendfile

class BaseXSendFileView(BaseDetailView):
    file_field = None
    send_as_attachment = None

    def get_file_field(self):
        return self.file_field

    def get_file_path(self, object):
        return getattr(object, self.get_file_field()).path

    def get_sendfile_kwargs(self, context):
        return dict(request=self.request,
                    filename=self.get_file_path(context['object']),
                    attachment=self.send_as_attachment)

    def render_to_response(self, context):
        return sendfile(**self.get_sendfile_kwargs(context))
