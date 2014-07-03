
from django.dispatch import Signal

user_tracking_event_happened = Signal(providing_args=["request", "event_name", "event_data"])

