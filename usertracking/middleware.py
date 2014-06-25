from tracking import generate_new_tracking_key, register_event

class UserTrackingMiddleware(object):

    def process_request(self, request):
        return None

    def process_response(self, request, response):
        """
        Only record when we return HTML pages. Set a cookie if not set
        """

        if 'text/html' in response.get('Content-Type', ''):

            tracking_id = None

            if 'user_tracking_id' not in request.COOKIES:

                tracking_id = generate_new_tracking_key()

                response.set_cookie('user_tracking_id', tracking_id)

                register_event(tracking_id=tracking_id, event_name='server_middleware_set_cookie', request=request)

                #set javascript callback behavior to check if the user has disabled cookies
                response.set_cookie('user_tracking_verify', tracking_id)

            else:
                tracking_id = request.COOKIES['user_tracking_id']

            event_data = {'url': request.path_info, 'method': request.method}

            register_event(tracking_id=tracking_id, event_name='server_middleware_page_view',event_data=event_data, request=request)

        return response
