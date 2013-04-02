"""
    RenderPDF helper class
    
"""
import os
import datetime
import cStringIO as StringIO
import ho.pisa as pisa
from cgi import escape
import logging

from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.views.generic.base import TemplateView

logger = logging.getLogger(__name__)


class RenderPDF(object):
    """
        class based view to render template in PDF format.
    """
    
    template_name = 'django_pdf/hello_world.html'
    assets_root = settings.MEDIA_ROOT
    assets_url = settings.MEDIA_ROOT
    
    def fetch_resources(self, uri, rel=''):
        """"
            Method return absolute path to resources.
        """
        absolute_path = os.path.join(self.assets_root,
            uri.replace(self.assets_url, ""))
        logger.debug(absolute_path)
        return absolute_path

    def render_to_response(self, context, **response_kwargs):
        context.update(response_kwargs)
        return self.render_to_pdf(context)

    def render_to_pdf(self, context):
        """
            renders pdf file
        """
        template = get_template(self.template_name)
        template_context = Context(context)
        html  = template.render(template_context)
        result = StringIO.StringIO()
        pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")),
            result, link_callback=self.fetch_resources)
        if not pdf.err:
            return HttpResponse(result.getvalue(), mimetype='application/pdf')
        return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))
