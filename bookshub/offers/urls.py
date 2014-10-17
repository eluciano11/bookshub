from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

# router.register(r'books/(?P<id>\d+)/images', views.BookImageViewSet)
router.register(r'offers', views.OffersViewSet)

urlpatterns = router.urls
