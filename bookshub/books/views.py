from rest_framework.response import Response

from . import serializers
from rest_framework import generics
from ..utils.response import ErrorResponse
from .models import Book


class CreateBookAPIView(generics.CreateAPIView):
    throttle_classes = ()
    permission_classes = ()
    serializer_class = serializers.CreateBookSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.DATA)

        if serializer.is_valid():
            return Response(serializer.object)

        return ErrorResponse(serializer.errors)


class BookAPIView(generics.RetrieveAPIView):
    model = Book
    serializer_class = serializers.BookSerializer

    def get_queryset(self):
        book = self.kwargs['id']
        return Book.objects.get(id=book)

    def get(self, request, id):
        serializer = self.get_serializer_context()
        return Response(serializer)
