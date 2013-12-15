"""
RenderPDF helper class
"""
import os
import cStringIO as StringIO
import xhtml2pdf.pisa as pisa
from cgi import escape
import logging

from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context

logger = logging.getLogger(__name__)


class RenderPDF(object):
    """
    Class based view to render template in PDF format
    Most of use cases as mixin, but can be used separately
    """
    # Template name for pdf rendering
    template_name = None
    assets_root = settings.STATIC_ROOT
    assets_url = settings.STATIC_URL

    def fetch_resources(self, uri, rel=''):
        """
        Returns absolute path to resources
        It search for resources in STATIC_ROOT, so you need run manage.py compilestatic first

        :arg uri Resource URL
        """
        absolute_path = os.path.join(self.assets_root, uri.replace(self.assets_url, ""))
        logger.debug(absolute_path)
        return absolute_path

    def render_to_response(self, context, **response_kwargs):
        context.update(response_kwargs)
        logger.debug(context)
        return HttpResponse(self.render_to_pdf(context), mimetype='application/pdf')

    def render_to_pdf(self, context, template_name=None):
        """
        Renders pdf file with given context
        """
        template = get_template(template_name or self.template_name)
        template_context = Context(context)
        html = template.render(template_context)
        result = StringIO.StringIO()
        pdf = pisa.pisaDocument(
            StringIO.StringIO(html.encode('UTF-8')),
            result,
            link_callback=self.fetch_resources,
            encoding='UTF-8'
        )

        if pdf.err:
            logger.error(pdf.err)
            return 'Error: <pre>%s</pre>' % escape(html)

        return result.getvalue()