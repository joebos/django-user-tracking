from datetime import datetime
import uuid
from tracking_async import set_warning_async, register_event_async
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.conf import settings
import json

from django.core.signing import Signer, BadSignature
from signals import user_tracking_event_happened

import django_rq

USER_TRACKING_ENABLED = getattr(settings, "USER_TRACKING_ENABLED", True)
USER_TRACKING_RQ_QUEUE_NAME = getattr(settings, "USER_TRACKING_RQ_QUEUE_NAME", 'django-user-tracking')

signer = Signer()
user_tracking_rq_queue = django_rq.get_queue(USER_TRACKING_RQ_QUEUE_NAME)


def generate_new_tracking_key():
    tracking_key = str(uuid.uuid1()).replace('-','')
    return signer.sign(tracking_key)

def verify_tracking_key(key):
    try:
        value = signer.unsign(key)
        return value
    except  BadSignature:
        return None


def register_event(tracking_id=None, event_name=None, event_data=None, request=None):

    if not USER_TRACKING_ENABLED:
        return

    #if hasattr(request, "user")
    user_id = getattr(request.user, "id") if hasattr(request, "user") and hasattr(request.user, 'id') else ''
    if user_id is None:
        user_id = ""

    tracking_id_unsigned = verify_tracking_key(tracking_id)

    if tracking_id_unsigned is None:
        log_error(message='tracking id cookie has been tampered', tracking_id=tracking_id, user_id=user_id)
        return

    params = {
        'tracking_id': tracking_id_unsigned,
        'user_id': user_id,
        'event_time': datetime.utcnow(),
        'event_name': event_name,
        'event_data': event_data,
    }

    if not request is None:
        params['request'] = get_tracking_data_from_request(request)
        params['session_id'] = request.session.session_key if hasattr(request, 'session') and request.session.session_key is not None else ''
        params['impersonate'] = request.impersonator if hasattr(request, 'impersonator') else ''

    user_tracking_rq_queue.enqueue(register_event_async, args=[], kwargs=params)
    user_tracking_event_happened.send(sender=register_event.__name__, request=request, event_name=event_name, event_data=event_data, kwargs=params)

def log_error(message='', tracking_id=None, user_id=None):

    if not USER_TRACKING_ENABLED:
        return

    user_tracking_rq_queue.enqueue(set_warning_async, args=[], kwargs={
        'message': message,
        'tracking_id': tracking_id,
        'user_id': user_id,
    })

def get_tracking_data_from_request(request):
    HTTP_KEYS_FOR_TRACKING = [
        'HTTP_X_FORWARDED_FOR',
        'HTTP_CLIENT_IP',
        'HTTP_X_FORWARDED',
        'HTTP_X_CLUSTER_CLIENT_IP',
        'HTTP_FORWARDED_FOR',
        'HTTP_FORWARDED',

        'HTTP_REFERER',
        'REQUEST_METHOD',
        'QUERY_STRING',
        'HTTP_HOST',
        'PATH_INFO',
        'HTTP_USER_AGENT',
        'HTTP_ACCEPT_LANGUAGE',
        'REMOTE_ADDR',
        'REMOTE_HOST',
        'REMOTE_USER',
    ]
    request_meta = request.META

    result = {}

    for key in HTTP_KEYS_FOR_TRACKING:
        if request_meta.has_key(key):
            result[key] = request_meta[key]

    result['IS_HTTPS'] = request.is_secure()

    return result


def register_user_logged_in(sender, request, user, **kwargs):
    """
    A signal receiver which triggers USER_LOGGED_IN
    """

    if 'user_tracking_id' in request.COOKIES:
        tracking_id = request.COOKIES['user_tracking_id']

        event_data = {
            'user_id' : user.id
        }

        register_event(tracking_id=tracking_id, event_name='server_signal_user_logged_in', request=request, event_data=event_data)
    else:
        log_error(message="User logged-in but doesn't have cookie set.", user_id = user.id)

user_logged_in.connect(register_user_logged_in, dispatch_uid="USER_TRACKING_USER_LOGGED_IN")

def register_user_logged_out(sender, request, user, **kwargs):
    """
    A signal receiver which triggers USER_LOGGED_OUT
    """
    if 'user_tracking_id' in request.COOKIES:
        cookie = request.COOKIES[ 'user_tracking_id' ]

        event_data = {
            'user_id' : user.id
        }

        register_event(tracking_id=cookie, event_name='server_signal_user_logged_out', request=request, event_data=event_data)
    else:
        log_error(message="User logged-out but doesn't have cookie set.", user_id= user.id)

user_logged_out.connect(register_user_logged_out, dispatch_uid="USER_TRACKING_USER_LOGGED_OUT")