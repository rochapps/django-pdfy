=====
PDF
=====

PDF is a simple Django app to render templates in PDF format. It overwrites the
render_to_response method and adds absoulte paths to give you access to your
css and images files.

Requirements
============
    1. pisa>=3.0.33
    2. pyPdf>=1.13
    3.reportlab>=2.6
    4. html5lib>=0.95
    5. mock (for testing)

Quick start
===========

1. Define ``MEDIA_ROOT`` and ``MEDIA_URL`` in your settings.py file
2. Subclass RenderPDF, set the ``template_name`` attribute.

For example, in myapp/views.py::

    from myapp.models import Transaction
    from pdf.views import RenderPDF
    from django.views.generic import ListView

    class TransactionListView(RenderPDF, ListView):
        # base_queryset is a queryset that contains all the objects that are
        # accessible by the API:
        template_name = 'mydpf.html'
        model = Transaction

In myapp/urls.py::

    from myapp.views import TransactionListView

    urlpatterns = patterns('',
        url(r'^transactions/$', TransactionListView.as_view()),
    )
