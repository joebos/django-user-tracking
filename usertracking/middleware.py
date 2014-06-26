from tracking import generate_new_tracking_key, register_event
from django.core.urlresolvers import reverse
from django.conf import settings

USER_TRACKING_LOG_HTML_FRAGMENT_RESPONSE = getattr(settings, "USER_TRACKING_LOG_HTML_FRAGMENT_RESPONSE", False)

class UserTrackingMiddleware(object):

    def process_request(self, request):
        return None

    def process_response(self, request, response):
        """
        Only record when we return HTML pages. Set a cookie if not set
        """

        if 'text/html' in response.get('Content-Type', ''):
            content = getattr(response, 'content', '')
            if USER_TRACKING_LOG_HTML_FRAGMENT_RESPONSE or content.find("<body") >= 0:
                url_request = request.path
                urls = [reverse('user_tracking_register_event'), reverse('user_tracking_verify')]

                found = False

                for url in urls:
                    if url_request.find(url) >= 0:
                        found = True
                        break

                if not found:
                    tracking_id = None
                    event_data = {'url': request.path_info, 'method': request.method}

                    if 'user_tracking_id' not in request.COOKIES:

                        tracking_id = generate_new_tracking_key()

                        response.set_cookie('user_tracking_id', tracking_id)

                        register_event(tracking_id=tracking_id, event_name='server_middleware_set_cookie', request=request)

                        #set javascript callback behavior to check if the user has disabled cookies
                        response.set_cookie('user_tracking_verify', tracking_id)

                    else:
                        tracking_id = request.COOKIES['user_tracking_id']

                    register_event(tracking_id=tracking_id, event_name='server_middleware_page_view',event_data=event_data, request=request)

        return response
