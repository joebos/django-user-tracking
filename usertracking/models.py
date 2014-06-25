from django.db import models
import jsonfield

class UserTrackingEvent(models.Model):

    tracking_id = models.CharField(max_length=32)
    user_id = models.CharField(max_length=32)
    session_id = models.CharField(max_length=32)

    event_time = models.DateTimeField(blank=False)
    event_name = models.CharField(max_length=255)
    event_data = jsonfield()

    request_data = jsonfield()
