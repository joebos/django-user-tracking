from django.db import models
from jsonfield import JSONField

class UserTrackingEvent(models.Model):

    tracking_id = models.CharField(max_length=255)
    user_id = models.CharField(max_length=255)
    session_id = models.CharField(max_length=255)

    event_time = models.DateTimeField(blank=False)
    event_name = models.CharField(max_length=255)
    event_data = JSONField(default='{}')

    request_data = JSONField(default='{}')
