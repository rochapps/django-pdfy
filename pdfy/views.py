"""
    RenderPDF helper class

"""
import cStringIO as StringIO
from cgi import escape
import logging
import os
import re

import ho.pisa as pisa

from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context

logger = logging.getLogger(__name__)


class RenderPDF(object):
    """
        class based view to render template in PDF format.
    """

    template_name = 'template.pdfy'

    def fetch_resources(self, uri, rel=''):
        """"
            Method return absolute path to resources.
        """
        if settings.STATIC_URL in uri:
            absolute_path = os.path.join(settings.STATIC_ROOT,
                uri.replace(settings.STATIC_URL, ""))
        else:
            absolute_path = os.path.join(settings.MEDIA_ROOT,
                uri.replace(settings.MEDIA_URL, ""))
        logger.debug(absolute_path)
        return absolute_path

    def render_to_response(self, context, **response_kwargs):
        context.update(response_kwargs)
        logger.debug(context)
        return self.render_to_pdf(context)

    def render_to_pdf(self, context):
        """
            renders pdfy file.
        """
        template = get_template(self.template_name)
        template_context = Context(context)
        html = template.render(template_context)
        result = StringIO.StringIO()
        pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")),
            result, link_callback=self.fetch_resources)
        if not pdf.err:
            return HttpResponse(result.getvalue(), mimetype='application/pdf')
        logger.error(pdf.err)
        return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))
