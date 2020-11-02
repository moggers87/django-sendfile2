# coding=utf-8

from tempfile import mkdtemp
from urllib.parse import unquote
import os
import shutil

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.http import Http404, HttpRequest, HttpResponse
from django.test import TestCase
from django.utils.encoding import smart_str

from .utils import _get_sendfile
from .utils import sendfile as real_sendfile


def sendfile(request, filename, **kwargs):
    # just a simple response with the filename
    # as content - so we can test without a backend active
    return HttpResponse(filename)


class TempFileTestCase(TestCase):

    def setUp(self):
        super(TempFileTestCase, self).setUp()
        self.TEMP_FILE = mkdtemp()
        self.TEMP_FILE_ROOT = os.path.join(self.TEMP_FILE, "root")
        os.mkdir(self.TEMP_FILE_ROOT)
        self.setSendfileRoot(self.TEMP_FILE_ROOT)

    def tearDown(self):
        super(TempFileTestCase, self).tearDown()
        if os.path.exists(self.TEMP_FILE_ROOT):
            shutil.rmtree(self.TEMP_FILE_ROOT)

    def setSendfileBackend(self, backend):
        '''set the backend clearing the cache'''
        settings.SENDFILE_BACKEND = backend
        _get_sendfile.cache_clear()

    def setSendfileRoot(self, path):
        '''set the backend clearing the cache'''
        settings.SENDFILE_ROOT = path

    def ensure_file(self, filename):
        path = os.path.join(self.TEMP_FILE_ROOT, filename)
        if not os.path.exists(path):
            open(path, 'w').close()
        return path


class TestSendfile(TempFileTestCase):

    def setUp(self):
        super(TestSendfile, self).setUp()
        # set ourselves to be the sendfile backend
        self.setSendfileBackend('django_sendfile.tests')

    def _get_readme(self):
        return self.ensure_file('testfile.txt')

    def test_backend_is_none(self):
        self.setSendfileBackend(None)
        with self.assertRaises(ImproperlyConfigured):
            real_sendfile(HttpRequest(), "notafile.txt")

    def test_root_is_none(self):
        self.setSendfileRoot(None)
        with self.assertRaises(ImproperlyConfigured):
            real_sendfile(HttpRequest(), "notafile.txt")

    def test_404(self):
        try:
            real_sendfile(HttpRequest(), 'fhdsjfhjk.txt')
        except Http404:
            pass

    def test_sendfile(self):
        response = real_sendfile(HttpRequest(), self._get_readme())
        self.assertTrue(response is not None)
        self.assertEqual('text/plain', response['Content-Type'])
        self.assertEqual('inline; filename="testfile.txt"', response['Content-Disposition'])
        self.assertEqual(self._get_readme(), smart_str(response.content))

    def test_set_mimetype(self):
        response = real_sendfile(HttpRequest(), self._get_readme(), mimetype='text/plain')
        self.assertTrue(response is not None)
        self.assertEqual('text/plain', response['Content-Type'])

    def test_set_encoding(self):
        response = real_sendfile(HttpRequest(), self._get_readme(), encoding='utf8')
        self.assertTrue(response is not None)
        self.assertEqual('utf8', response['Content-Encoding'])

    def test_inline_filename(self):
        response = real_sendfile(HttpRequest(), self._get_readme(), attachment_filename='tests.txt')
        self.assertTrue(response is not None)
        self.assertEqual('inline; filename="tests.txt"', response['Content-Disposition'])

    def test_attachment(self):
        response = real_sendfile(HttpRequest(), self._get_readme(), attachment=True)
        self.assertTrue(response is not None)
        self.assertEqual('attachment; filename="testfile.txt"', response['Content-Disposition'])

    def test_attachment_filename_false(self):
        response = real_sendfile(HttpRequest(), self._get_readme(), attachment=True,
                                 attachment_filename=False)
        self.assertTrue(response is not None)
        self.assertEqual('attachment', response['Content-Disposition'])

    def test_attachment_filename(self):
        response = real_sendfile(HttpRequest(), self._get_readme(), attachment=True,
                                 attachment_filename='tests.txt')
        self.assertTrue(response is not None)
        self.assertEqual('attachment; filename="tests.txt"', response['Content-Disposition'])

    def test_attachment_filename_unicode(self):
        response = real_sendfile(HttpRequest(), self._get_readme(), attachment=True,
                                 attachment_filename='test’s.txt')
        self.assertTrue(response is not None)
        self.assertEqual('attachment; filename="tests.txt"; filename*=UTF-8\'\'test%E2%80%99s.txt',
                         response['Content-Disposition'])


class TestSimpleSendfileBackend(TempFileTestCase):

    def setUp(self):
        super().setUp()
        self.setSendfileBackend('django_sendfile.backends.simple')

    def test_correct_file(self):
        filepath = self.ensure_file('readme.txt')
        response = real_sendfile(HttpRequest(), filepath)
        self.assertTrue(response is not None)

    def test_containing_unicode(self):
        filepath = self.ensure_file(u'péter_là_gueule.txt')
        response = real_sendfile(HttpRequest(), filepath)
        self.assertTrue(response is not None)

    def test_sensible_file_access_in_simplesendfile(self):
        filepath = self.ensure_file('../passwd')
        with self.assertRaises(Http404):
            real_sendfile(HttpRequest(), filepath)


class TestXSendfileBackend(TempFileTestCase):

    def setUp(self):
        super(TestXSendfileBackend, self).setUp()
        self.setSendfileBackend('django_sendfile.backends.xsendfile')

    def test_correct_file_in_xsendfile_header(self):
        filepath = self.ensure_file('readme.txt')
        response = real_sendfile(HttpRequest(), filepath)
        self.assertTrue(response is not None)
        self.assertEqual(filepath, response['X-Sendfile'])

    def test_xsendfile_header_containing_unicode(self):
        filepath = self.ensure_file(u'péter_là_gueule.txt')
        response = real_sendfile(HttpRequest(), filepath)
        self.assertTrue(response is not None)
        self.assertEqual(smart_str(filepath), response['X-Sendfile'])


class TestNginxBackend(TempFileTestCase):

    def setUp(self):
        super(TestNginxBackend, self).setUp()
        self.setSendfileBackend('django_sendfile.backends.nginx')
        settings.SENDFILE_URL = '/private'

    def test_sendfile_url_not_set(self):
        settings.SENDFILE_URL = None
        filepath = self.ensure_file('readme.txt')
        response = real_sendfile(HttpRequest(), filepath)
        self.assertTrue(response is not None)
        self.assertEqual(response.content, b'')
        self.assertEqual(os.path.join(self.TEMP_FILE_ROOT, 'readme.txt'),
                         response['X-Accel-Redirect'])

    def test_correct_url_in_xaccelredirect_header(self):
        filepath = self.ensure_file('readme.txt')
        response = real_sendfile(HttpRequest(), filepath)
        self.assertTrue(response is not None)
        self.assertEqual(response.content, b'')
        self.assertEqual('/private/readme.txt', response['X-Accel-Redirect'])

    def test_xaccelredirect_header_containing_unicode(self):
        filepath = self.ensure_file(u'péter_là_gueule.txt')
        response = real_sendfile(HttpRequest(), filepath)
        self.assertTrue(response is not None)
        self.assertEqual(response.content, b'')
        self.assertEqual('/private/péter_là_gueule.txt', unquote(response['X-Accel-Redirect']))


class TestModWsgiBackend(TempFileTestCase):

    def setUp(self):
        super(TestModWsgiBackend, self).setUp()
        self.setSendfileBackend('django_sendfile.backends.mod_wsgi')
        settings.SENDFILE_URL = '/private'

    def test_sendfile_url_not_set(self):
        settings.SENDFILE_URL = None
        filepath = self.ensure_file('readme.txt')
        response = real_sendfile(HttpRequest(), filepath)
        self.assertTrue(response is not None)
        self.assertEqual(response.content, b'')
        self.assertEqual(os.path.join(self.TEMP_FILE_ROOT, 'readme.txt'),
                         response['Location'])

    def test_correct_url_in_location_header(self):
        filepath = self.ensure_file('readme.txt')
        response = real_sendfile(HttpRequest(), filepath)
        self.assertTrue(response is not None)
        self.assertEqual(response.content, b'')
        self.assertEqual('/private/readme.txt', response['Location'])

    def test_location_header_containing_unicode(self):
        filepath = self.ensure_file(u'péter_là_gueule.txt')
        response = real_sendfile(HttpRequest(), filepath)
        self.assertTrue(response is not None)
        self.assertEqual(response.content, b'')
        self.assertEqual('/private/péter_là_gueule.txt', unquote(response['Location']))
