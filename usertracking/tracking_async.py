
from django.contrib.auth.models import User
import json

from models import UserTrackingEvent

import logging
logger = logging.getLogger(__name__)


def set_warning_async(**kwargs):

    u = User.objects.get(pk=kwargs['user_id'])

    msg = "%s | (%s) %s %s last_login: %s " % (kwargs['message'],
                                     u.username or '',
                                     u.first_name or '',
                                     u.last_name or '',
                                     u.last_login or '')
    logger.warning(msg)

    return

def register_event_async(**kwargs):

    tracking_id = kwargs.get('tracking_id', '')
    user_id = kwargs.get('user_id', '')
    session_id = kwargs.get('session_id', '')

    event_name = kwargs.get('event_name', '')
    event_time = kwargs.get('event_time', None)
    event_data = kwargs.get('event_data', {})
    impersonator = kwargs.get('impersonate', '')
    server_name = kwargs.get('server_name', '')
    client_ip = kwargs.get('client_ip', '')
    if event_data is None:
        event_data = {}
    event_data["server_name"] = server_name
    event_data["client_ip"] = client_ip

    request_data = kwargs.get('request', {})

    if kwargs['event_name'] == 'server_middleware_page_view':
        if request_data is not None:
            if '/favicon.ico' in request_data['PATH_INFO']:
                return
            if '/admin' in request_data['PATH_INFO']:
                return

    try:
        tracking_event = UserTrackingEvent()

        tracking_event.tracking_id = tracking_id
        tracking_event.user_id = user_id
        tracking_event.session_id = session_id
        tracking_event.impersonator = impersonator

        tracking_event.event_time = event_time
        tracking_event.event_name = event_name
        tracking_event.event_data = event_data

        tracking_event.request_data = request_data

        tracking_event.save()

    except Exception as e:
        print "could not save tracking"
        raise
