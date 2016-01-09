
from django.conf.urls import url, patterns
from views import VerifyView, RegisterEventView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = patterns('',
    url(r'^user-tracking/verify$', VerifyView.as_view(), name='user_tracking_verify'),
    url(r'^user-tracking/register-event$', csrf_exempt(RegisterEventView.as_view()), name='user_tracking_register_event'),
)

