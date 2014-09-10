from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(
        r'^admin/',
        include(admin.site.urls)
    ),
    url(
        r'^accounts/',
        include('allauth.urls')
    ),
    url(
        r'^api/',
        include('bookshub.users.urls')
    )
)

if settings.ENVIRONMENT == 'Production':
    urlpatterns += (
        url(
            r'^api/docs/',
            include('rest_framework_swagger.urls')
        ),
    )
