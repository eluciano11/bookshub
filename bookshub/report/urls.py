from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    '',
    url(r'^report/user/$',
        views.ReportUserAPIView.as_view(), name='report'),
)
