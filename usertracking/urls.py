
from django.conf.urls.defaults import url, patterns
from views import VerifyView, RegisterEventView
from django.views.decorators.csrf import csrf_view_exempt

urlpatterns = patterns('brand.views',
    url(r'^user-tracking/verify$', VerifyView.as_view(), name='user_tracking_verify'),
    url(r'^user-tracking/register-event$', RegisterEventView.as_view(), name='user_tracking_register_event'),
)

