from django.views.generic import View
from django.http import HttpResponse
from tracking import register_event, generate_new_tracking_key

class VerifyView(View):
    '''
    View called by javascript to verify that cookies are enabled along with javascript
    '''

    def post(self, request, *args, **kwargs):

        tracking_id = self.request.COOKIES.get('user_tracking_id', None)
        register_event(tracking_id, event_name='VERIFY_COOKIE', request=self.request)
        response = HttpResponse('Verified')
        response.delete_cookie('user_tracking_verify')

        return response

class RegisterEventView(View):
    '''
    View called by javascript to verify that cookies are enabled along with javascript
    '''

    def post(self, request, *args, **kwargs):

        event_name = self.request.POST.get('event_name', None)
        raw_event_data = self.request.POST.get('event_data', None)

        event_data = None

        if raw_event_data is not None:
            #truncate at 1024 character to avoid malicious content
            event_data = (raw_event_data[:202400] + '..') if len(raw_event_data) > 202400 else raw_event_data
        else:
            event_data = raw_event_data

        tracking_id = self.request.COOKIES.get('user_tracking_id', None)
        if tracking_id is None:
            tracking_id = generate_new_tracking_key()

        register_event(tracking_id=tracking_id, event_name=event_name, request=self.request, event_data=event_data)
        response = HttpResponse('OK')
        response.set_cookie('user_tracking_id', tracking_id)

        return response