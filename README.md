django-user-tracking
====================

A user tracking package focusing on client side user tracking for Django.

Installation

    pip install -e git+git@github.com:joebos/django-user-tracking.git#egg=django-user-tracking

Configuration

    urls.py:

        url(r'^', include('usertracking.urls')),

    settings.py:

        INSTALLED_APPS = [
            "django_rq",
            'usertracking',
        ]


        MIDDLEWARE_CLASSES = [
            "usertracking.middleware.UserTrackingMiddleware",

        ]

        RQ_QUEUES = {
            'django-user-tracking': {
                'HOST': 'localhost',
                'PORT': 6379,
                'DB': 0,
            }
        }

