
from django.contrib.auth.models import User
import json

from models import UserTrackingEvent

import logging
logger = logging.getLogger(__name__)

from django.conf import settings
USER_TRACKING_MONGO_URL = getattr(settings, "USER_TRACKING_MONGO_URL", '')

import time
import datetime

from restclient import GET, POST, PUT, DELETE
from time import mktime
import sys

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
    event_data = kwargs.get('event_data', "{}")
    impersonator = kwargs.get('impersonate', '')
    server_name = kwargs.get('server_name', '')
    client_ip = kwargs.get('client_ip', '')
    ref = kwargs.get('ref', '')

    if event_data is None:
        event_data = {}
    else:
        if isinstance(event_data, basestring):
            event_data = json.loads(event_data)
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
        tracking_event.ref = ref
        tracking_event.session_id = session_id
        tracking_event.impersonator = impersonator

        tracking_event.event_time = event_time
        tracking_event.event_name = event_name
        tracking_event.event_data = event_data

        tracking_event.request_data = request_data

        if USER_TRACKING_MONGO_URL == "":
            tracking_event.save()
        else:
            tracking_event.event_time = tracking_event.event_time.isoformat()
            tracking_event.impersonator = tracking_event.impersonator.username if tracking_event.impersonator else ""
            tracking_event_json = json.loads(json.dumps(tracking_event, default=lambda o: o.__dict__, cls=DateTimeEncoder))
            log_tracking_event_to_mongodb(tracking_event_json)

    except Exception as e:
        print "could not save tracking"
        raise

class DateTimeEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return int(mktime(obj.timetuple()))

        return json.JSONEncoder.default(self, obj)

def log_tracking_event_to_mongodb(logging_data):
    try:
        cur_time = datetime.datetime.utcnow()
        cur_timestamp = time.mktime(cur_time.timetuple())
        logging_data["time"] = str(cur_time)
        logging_data["timestamp"] = (cur_timestamp)

        mongo_api_response = POST(USER_TRACKING_MONGO_URL, async=False, resp=True, params=logging_data, headers={'Content-Type': 'application/json'})

        return {'status_code': mongo_api_response[0].status}
    except:
        logging_data_str = json.dumps(logging_data, indent=4, sort_keys=False, cls=DateTimeEncoder)
        print "Logging user tracking event Error: {0}: {0}".format( sys.exc_info()[0], logging_data_str)
