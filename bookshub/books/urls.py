from django.conf.urls import patterns

from . import views

urlpatterns = patterns(
    # Prefix
    '',
    (
        r'create/$',
        views.CreateBookAPIView.as_view()
    ),
)
