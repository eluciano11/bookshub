from rest_framework.viewsets import ModelViewSet

from .models import Book
from .serializers import BookSerializer
# from ..utils.response import ErrorResponse


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # permission_classes = (BoardPermission, )

    def post_save(self, *args, **kwargs):
        if 'tags' in self.request.DATA:
            self.object.tags.set(*self.request.DATA['tags'])
        return super(BookViewSet, self).post_save(*args, **kwargs)
