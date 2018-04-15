from django.views.generic.detail import BaseDetailView
from sendfile import sendfile


class XSendFileView(BaseDetailView):
    """
    Provide the ability to download any file. In the remaining range it
    behaves like BaseDetailView.

    **Class Settings**

    ``XSendFielView.file_field``
        *Default*: ``'None'``. A model field name which contains file.

    ``XSendFielView.send_as_attachment``
        *Default*: ``'None'``. If is True the content-disposition header will be set.

    """
    file_field = None
    send_as_attachment = None

    def get_file_field(self):
        """
        :return: A model field name which contains file.
        """
        return self.file_field

    def get_file_path(self, object):
        """
        :param object: A object of view.
        :return: A file path from object.
        """
        return getattr(object, self.get_file_field()).path

    def get_sendfile_kwargs(self, context):
        """
        :param context: standard django context dict
        :return: A kwargs of sendfile function.
        """
        return dict(request=self.request,
                    filename=self.get_file_path(context['object']),
                    attachment=self.send_as_attachment)

    def render_to_response(self, context):
        return sendfile(**self.get_sendfile_kwargs(context))
