"""
    RenderPDF helper class

"""
import logging
import os
import cStringIO as StringIO
from cgi import escape

import xhtml2pdf.pisa as pisa

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

    def fetch_resources(self, uri, rel=''):
        """"
        Returns absolute path to resources.

        It search for resources in STATIC_ROOT and MEDIA_ROOT, so you may
        need run manage.py collectstatic first.

        :arg uri Resource URL
        """
        if settings.STATIC_URL in uri:
            absolute_path = os.path.join(
                settings.STATIC_ROOT,
                uri.replace(settings.STATIC_URL, "")
            )
        else:
            absolute_path = os.path.join(
                settings.MEDIA_ROOT,
                uri.replace(settings.MEDIA_URL, "")
            )
        logger.debug(absolute_path)
        return absolute_path

    def render_to_response(self, context, **response_kwargs):
        context.update(response_kwargs)
        context.update({
            "STATIC_URL": settings.STATIC_URL,
            "MEDIA_URL": settings.MEDIA_URL,
        })
        logger.debug(context)
        return HttpResponse(self.render_to_pdf(context), mimetype='application/pdf')

    def render_to_pdf(self, context):
        """
        Renders pdf file with given context
        """
        template = get_template(self.template_name)
        template_context = Context(context)
        html = template.render(template_context)
        result = StringIO.StringIO()
        pdf = pisa.pisaDocument(
            StringIO.StringIO(html.encode("UTF-8")),
            result,
            link_callback=self.fetch_resources,
            encoding='UTF-8'
        )
        if pdf.err:
            logger.error(pdf.err)
            return 'We had some errors<pre>%s</pre>' % escape(html)
        return result.getvalue()
