from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register(r'books', views.BookViewSet)

urlpatterns = router.urls
