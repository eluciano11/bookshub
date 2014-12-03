from django.conf.urls import patterns

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register(r'cart', views.OrderItemViewSet)

urlpatterns = router.urls

urlpatterns += patterns(
    # Prefix
    '',
    (
        r'checkout/$',
        views.BuyItemsInCartView.as_view()
    ),
)
