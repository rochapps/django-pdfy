========================
django-pdfy
========================

django-pdf lets you to render any view as pdf, css and images are also available
in your templates.

.. image::
    https://secure.travis-ci.org/rochapps/django-pdfy.png
    :alt: Build Status
        :target: https://secure.travis-ci.org/rochapps/django-pdf

Requirements
============
    1. django>=1.3
    2. xhtml2pdf==0.0.5
    5. mock (for testing)

Install
=======
Use pip to install::

    pip install django-pdfy

Quick start
===========

1. Define ``STATIC_ROOT`` and ``STATIC_URL`` in your settings.py file.
2. Subclass RenderPDF, set the ``template_name`` attribute.

For example, in myapp/views.py::

    from myapp.models import Transaction
    from pdfy.views import RenderPDF
    from django.views.generic import ListView

    class TransactionListView(RenderPDF, ListView):
        template_name = 'mypdf.html'
        model = Transaction

In myapp/urls.py::

    from myapp.views import TransactionListView

    urlpatterns = patterns('',
        url(r'^transactions/$', TransactionListView.as_view()),
    )


Running the Tests
------------------------------------

You can run the tests with via::

    python setup.py test

or::

    python runtests.py


License
--------------------------------------

django-secure-input is released under the BSD License. See the
`LICENSE <https://github.com/rochapps/django-pdf/blob/master/LICENSE>`_ file for more details.


Contributing
--------------------------------------

If you think you've found a bug or are interested in contributing to this project
check out `django-pdfy on Github <https://github.com/rochapps/django-pdfy>`_.

Development sponsored by `RochApps, LLC
<http://www.rochapps.com/services>`_.
