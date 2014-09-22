from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

<<<<<<< HEAD
from .models import Book, Requested
from .permissions import BookPermission
from .serializers import BookSerializer, RequestedSerializer
=======
from .models import Book, Image
from .permissions import BookPermission, ImagePermission
from .serializers import BookSerializer, ImageSerializer
>>>>>>> FETCH_HEAD
from ..utils.response import ErrorResponse


class BookViewSet(ModelViewSet):
    model = Book
    serializer_class = BookSerializer
    permission_classes = (BookPermission, )

    def get_queryset(self):
        return Book.objects.filter(owner=self.request.user)

    def post_save(self, *args, **kwargs):
        if 'tags' in self.request.DATA:
            self.object.tags.set(*self.request.DATA['tags'])
        return super(BookViewSet, self).post_save(*args, **kwargs)

    def post(self, request):
        serializer = self.get_serializer(data=request.DATA)

        if serializer.is_valid():
            return Response(serializer.object)

        return ErrorResponse(serializer.errors)


<<<<<<< HEAD
class RequestedViewSet(ModelViewSet):
    model = Requested
    serializer_class = RequestedSerializer
    permission_classes = ()

    def post(self, request):
        serializer = self.get_serializer(data=request.DATA)

        if serializer.is_valid() and request.user.is_authenticated():
            return Response(serializer.object)

        return ErrorResponse(serializer.errors)
=======
class BookImageViewSet(ModelViewSet):
    model = Image
    serializer_class = ImageSerializer
    permission_classes = (ImagePermission, )

    def get_queryset(self):
        return Image.objects.filter(
            book=self.kwargs['id'], book__owner=self.request.user)

    def pre_save(self, obj, *args, **kwargs):
        obj.book_id = self.kwargs['id']
>>>>>>> FETCH_HEAD
