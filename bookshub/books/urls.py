from django.conf.urls import patterns, url
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register(r'books/(?P<id>\d+)/reviews', views.ReviewViewSet)
router.register(r'books/requested', views.RequestedViewSet)

urlpatterns = router.urls

urlpatterns += patterns(
    '',
    url(r'^books/$',
        views.CreateBookAPIView.as_view(), name='books'),
    url(r'^books/(?P<id>\d+)/$',
        views.SpecificBookAPIView.as_view(), name='specific_book'),
    url(r'^search/$',
        views.SearchAPIView.as_view(), name='search'),
    url(r'^search/autocomplete/$',
        views.SearchAutoCompleteAPIView.as_view(), name='search_autocomplete'),
    url(r'^books/top/requested/$',
        views.TopRequestedAPIView.as_view(), name='top_requested'),
    url(r'^books/top/recommended/$',
        views.TopRecommendedAPIView.as_view(), name='top_recommended'),
    #     views.TopSellersAPIView.as_view(), name='top_sellers'),
)
