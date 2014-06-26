
from django.conf.urls import url, patterns
from views import VerifyView, RegisterEventView

urlpatterns = patterns('',
    url(r'^user-tracking/verify$', VerifyView.as_view(), name='user_tracking_verify'),
    url(r'^user-tracking/register-event$', RegisterEventView.as_view(), name='user_tracking_register_event'),
)

