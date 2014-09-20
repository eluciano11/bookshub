from django.conf.urls import patterns

from . import views

urlpatterns = patterns(
    # Prefix
    '',
    (
        r'create/$',
        views.CreateBookAPIView.as_view()
    ),
    (
        r'(?P<id>[0-9]+)/$',
        views.BookAPIView.as_view()
    ),
    # (
    #     r'delete/(?P<id>[0-9]+)/$',
    #     views.DeleteBookAPIView.as_view()
    # ),
    # (
    #     r'edit/(?P<id>[0-9]+)/$',
    #     views.EditBookAPIView.as_view()
    # ),
)
