from django.contrib import admin
from models import UserTrackingEvent


class UserTrackingEventAdmin(admin.ModelAdmin):
    list_display = ('tracking_id', 'user_id', 'session_id', 'event_time', 'event_name', 'event_data', 'request_data')
    date_hierarchy = 'event_time'

admin.site.register(UserTrackingEvent, UserTrackingEventAdmin)