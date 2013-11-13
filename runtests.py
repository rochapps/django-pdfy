#!/usr/bin/env python
import os
import sys

from django.conf import settings

ROOT_PATH = os.path.dirname(__file__)

if not settings.configured:
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=(
            'pdfy',
        ),
        TEMPLATE_DIRS = (os.path.join(ROOT_PATH, 'pdfy/tests/templates'),),
        STATIC_ROOT = os.path.join(ROOT_PATH, 'static'),
        STATIC_URL = '/static/',
        SITE_ID=1,
        SECRET_KEY='this-is-just-for-tests-so-not-that-secret',
    )


from django.test.utils import get_runner


def runtests():
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1, interactive=True, failfast=False)
    failures = test_runner.run_tests(['pdfy', ])
    sys.exit(failures)


if __name__ == '__main__':
    runtests()
