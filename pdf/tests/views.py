import unittest
from mock import patch

from django.conf import settings
from django.test import TestCase
from django.test.client import RequestFactory

from pdf.views import RenderPDF


class RenderPDFTests(TestCase):
    """
        Tests for RenderPDF class
    """
    def setUp(self):
        settings.MEDIA_ROOT = '/home/rochapps/www/pdf/media'
        settings.MEDIA_URL = '/media/'
        self.template = 'django_pdf/hello_world.html'
        self.factory = RequestFactory()
        self.url = '/'
        
    def test_fetch_resources(self):
        request = self.factory.get(self.url)
        view = RenderPDF(request=request)
        asset_url = '/media/logo.png'
        absolute_path = view.fetch_resources(uri=asset_url)
        self.assertEqual(
            absolute_path, 
            '/home/rochapps/www/pdf/media/logo.png'
        )
        
    def test_render_to_response(self):
        """
            render_to_response should call render_to_pdf
        """
        request = self.factory.get(self.url)
        view = RenderPDF(request=request)
        view.template_name = self.template
        context = {}
        with patch.object(RenderPDF, 'render_to_pdf') as render_to_pdf:
            view.render_to_response(context)
            render_to_pdf.assert_called_once_with()
            
    def test_render_to_pdf(self):
        """
            test the mimetype of the output
        """
        request = self.factory.get(self.url)
        view = RenderPDF(request=request)
        view.template_name = self.template
        context = {}
        response = view.render_to_pdf(**context)
        self.assertEqual(response.get('content-type'), 'application/pdf')
        self.assertIn(
            'ReportLab Generated PDF document http://www.reportlab.com',
            response.content)
