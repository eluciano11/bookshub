from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from djrill import DjrillAdminSite

admin.site = DjrillAdminSite()
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(
        r'^admin/',
        include(admin.site.urls)
    ),
    url(
        r'^api/',
        include('bookshub.users.urls')
    ),
    url(
        r'^api/',
        include('bookshub.books.urls')
    ),
)

if settings.ENVIRONMENT == 'Production':
    urlpatterns += (
        url(
            r'^api/docs/',
            include('rest_framework_swagger.urls')
        ),
    )
