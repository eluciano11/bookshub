from django.conf.urls import patterns, url
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register(r'books/(?P<id>\d+)/images', views.BookImageViewSet)
router.register(r'books/requested', views.RequestedViewSet)
router.register(r'books', views.BookViewSet)

urlpatterns = router.urls

urlpatterns += patterns(
    '',
    url(r'^search/$',
        views.SearchAPIView.as_view(), name='search'),
    url(r'^books/top/requested/$',
        views.TopRequestedAPIView.as_view(), name='top_requested'),
    url(r'^books/top/recommended/$',
        views.TopRecommendedAPIView.as_view(), name='top_recommended'),
    url(r'^books/(?P<id>\d+)/reviews/$',
        views.AllReviewsAPIView.as_view(), name='book_reviews'),
    # url(r'^books/(?P<id>\d+)/reviews/(?P<id_review>\d+)/$',
    #     views.SpecificReviewAPIView.as_view(), name='book_review'),
    # url(r'^books/top/sellers/$',
    #     views.TopSellersAPIView.as_view(), name='top_sellers'),
)
