from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register(r'cart', views.OrderItemViewSet)

urlpatterns = router.urls
