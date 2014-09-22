from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

<<<<<<< HEAD
router.register(r'books/requested', views.RequestedViewSet)
=======
router.register(r'books/(?P<id>\d+)/images', views.BookImageViewSet)
>>>>>>> FETCH_HEAD
router.register(r'books', views.BookViewSet)

urlpatterns = router.urls
