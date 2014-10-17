from rest_framework import generics
# from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
# from rest_framework import status

from .models import Book, Requested, Image, Review, Viewed
from .permissions import BookPermission, ImagePermission
from .serializers import BookSerializer, RequestedSerializer, ImageSerializer, ReviewSerializer, BookSimpleSerializer
from ..utils.response import ErrorResponse


class CreateBookAPIView(generics.CreateAPIView):
    model = Book
    serializer_class = BookSerializer
    permission_classes = (BookPermission, )


class SpecificBookAPIView(generics.RetrieveAPIView):
    model = Book
    serializer_class = BookSerializer
    lookup_field = 'id'


class RequestedViewSet(ModelViewSet):
    model = Requested
    serializer_class = RequestedSerializer
    permission_classes = ()

    def post(self, request):
        serializer = self.get_serializer(data=request.DATA)

        if serializer.is_valid() and request.user.is_authenticated():
            return Response(serializer.object)

        return ErrorResponse(serializer.errors)


class BookImageViewSet(ModelViewSet):
    model = Image
    serializer_class = ImageSerializer
    permission_classes = (ImagePermission, )

    def get_queryset(self):
        return Image.objects.filter(
            book=self.kwargs['id'], book__owner=self.request.user)

    def pre_save(self, obj, *args, **kwargs):
        obj.book_id = self.kwargs['id']


class ReviewViewSet(ModelViewSet):
    model = Review
    serializer_class = ReviewSerializer

    def initialize_request(self, request, *args, **kwargs):
        """
        Disable authentication and permissions for `create` action.
        """
        initialized_request = super(
            ReviewViewSet, self).initialize_request(request, *args, **kwargs)

        user = request.user
        request_method = request.method.lower()
        action = self.action_map.get(request_method)

        if not user.is_authenticated() and (action == 'list' or action == 'retrive'):
            self.authentication_classes = ()
            self.permission_classes = (IsAuthenticatedOrReadOnly,)

        return initialized_request

    def post(self, request):
        serializer = self.get_serializer(data=request.DATA)

        if serializer.is_valid():
            return Response(serializer.object)

        return ErrorResponse(serializer.errors)


class SearchAPIView(generics.ListAPIView):
    serializer_class = BookSimpleSerializer
    permission_classes = ()

    def get_queryset(self):
        search_by = self.request.QUERY_PARAMS.get('search_by')
        search_string = self.request.QUERY_PARAMS.get('search_string')

        if search_by != 'isbn_10' and search_by != 'isbn_13':
            field_specification = search_by + '__icontains'
            return Book.objects.filter(**{
                field_specification: search_string})
        else:
            field_specification = search_by + '__iexact'
            return Book.objects.filter(**{
                field_specification: search_string})


class TopRequestedAPIView(generics.ListAPIView):
    model = Requested
    queryset = Requested.objects.order_by('-count')[:5]
    serializer_class = RequestedSerializer
    permission_classes = ()


class TopRecommendedAPIView(generics.ListAPIView):
    model = Book
    serializer_class = BookSimpleSerializer
    permission_classes = ()

    def get_queryset(self):
        viewed = Viewed.objects.filter(user=self.request.user)
        category_recommended = []
        top_reviewed = []
        for data in viewed:
            if data.book.category not in category_recommended:
                category_recommended.append(data.book.category)
                top_reviewed.append(
                    Review.objects.filter(
                        book__category=data.book.category).order_by('-score')[:5])


# class TopSellersAPIView(generics.ListAPIView):
#     model = Book
#     serializer_class = BookSerializer
#     permission_classes = ()
#     queryset = Requested.objects.order_by('-count')[:5]
