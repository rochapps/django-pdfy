from mock import patch

from django.conf import settings
from django.test import TestCase
from django.test.client import RequestFactory

from pdfy.views import RenderPDF


class RenderPDFTests(TestCase):
    """
    Tests for RenderPDF class
    """
    def setUp(self):
        self.template = 'template.pdf'
        self.factory = RequestFactory()
        self.url = '/'

    def test_fetch_resources(self):
        view = RenderPDF()
        asset_url = '/static/logo.png'
        absolute_path = view.fetch_resources(uri=asset_url)
        self.assertEqual(
            absolute_path,
            settings.STATIC_ROOT + '/logo.png'
        )

    def test_render_to_response(self):
        """
        Render_to_response should call render_to_pdf
        """
        view = RenderPDF()
        view.template_name = self.template
        context = {}
        with patch.object(RenderPDF, 'render_to_pdf') as render_to_pdf:
            view.render_to_response(context)
            render_to_pdf.assert_called_once_with(context)

    def test_pdf(self):
        """
        Test the mimetype of the output and verifies that it is a
        ReportLab Generated PDF document.
        """
        view = RenderPDF()
        view.template_name = self.template
        response = view.render_to_response({})
        self.assertEqual(response.get('content-type'), 'application/pdf')
        self.assertIn(
            b'ReportLab Generated PDF document http://www.reportlab.com',
            response.content
        )
