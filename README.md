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


        USER_TRACKING_RQ_QUEUE_NAME = 'django-user-tracking-app'

        USER_TRACKING_ENABLED = True
        USER_TRACKING_LOG_HTML_FRAGMENT_RESPONSE = False



Client side javascript:

        <script type="text/javascript" src="{% static "js/user_tracking.js" %}"></script>

        user_tracking.register_event(<event_name>, <event_data_json>);

Example:

        <script>
          function hyperlink_event(button, event){
            var text = $(button).html();
            var id= $(button).attr("id");
            user_tracking.register_event(event, {"url": window.location.pathname, "object": "button", "text": text , "id": id});
          }

          function button_event(link, event){
            var text = $(link).html();
            var href= $(link).attr("href");
            user_tracking.register_event(event, {"url": window.location.pathname, "object": "hyperlink", "text": text , "href": href});
          }

          $(function(){
            $('a').on('click',
                function() {
                    hyperlink_event(this, 'click')
                }
            );

            $('button').on('click',
                function() {
                    button_event(this, 'click')
                }
            );

          });

       </script>



