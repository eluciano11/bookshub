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
    url(
        r'^api/',
        include('bookshub.contact.urls')
    ),
    url(
        r'^api/',
        include('bookshub.report.urls')
    ),
    url(
        r'^api/',
        include('bookshub.offers.urls')
    ),
    url(
        r'^api/',
        include('bookshub.cart.urls')
    ),
    url(
        r'^payments/',
        include('djstripe.urls', namespace="djstripe")
    ),
    url(
        r'^api-docs/',
        include('rest_framework_swagger.urls')
    ),
)

if settings.ENVIRONMENT != 'PRODUCTION':
    urlpatterns += (
        url(
            r'^(?P<path>.*)$',
            'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )
