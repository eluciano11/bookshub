from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register(r'offers/(?P<id>\d+)/images', views.OfferImageViewSet)
router.register(r'offers', views.OfferViewSet)

urlpatterns = router.urls
