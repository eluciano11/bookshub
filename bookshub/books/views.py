import json
from itertools import chain

from django.db.models import Q

from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Book, Requested, Review, Viewed
from .serializers import (BookSerializer, RequestedSerializer,
                          ReviewSerializer, BookSimpleSerializer,
                          SearchSerializer)
from ..utils.response import ErrorResponse
from ..utils.search_api import SearchWrapper


class CreateBookAPIView(generics.CreateAPIView):
    model = Book
    serializer_class = BookSerializer
    permission_classes = ()
    authentication_classes = ()


class SpecificBookAPIView(generics.RetrieveAPIView):
    model = Book
    serializer_class = BookSerializer
    lookup_field = 'id'
    authentication_classes = ()
    permission_classes = ()


class RequestedViewSet(ModelViewSet):
    model = Requested
    serializer_class = RequestedSerializer
    permission_classes = ()
    filter_fields = ('title', )

    def initialize_request(self, request, *args, **kwargs):
        """
        Disable authentication and permissions for `list or retrieve` action.
        """
        initialized_request = super(
            RequestedViewSet, self).initialize_request(request, *args, **kwargs)

        user = request.user
        request_method = request.method.lower()
        action = self.action_map.get(request_method)

        if not user.is_authenticated() and\
                (action == 'list' or action == 'retrieve'):
            self.authentication_classes = ()
            self.permission_classes = (IsAuthenticatedOrReadOnly,)

        return initialized_request


class ReviewViewSet(ModelViewSet):
    model = Review
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return self.model.objects.filter(book=self.kwargs['book_id'])

    def initialize_request(self, request, *args, **kwargs):
        """
        Disable authentication and permissions for `create` action.
        """
        initialized_request = super(
            ReviewViewSet, self).initialize_request(request, *args, **kwargs)

        user = request.user
        request_method = request.method.lower()
        action = self.action_map.get(request_method)

        if not user.is_authenticated() and\
                (action == 'list' or action == 'retrieve'):
            self.authentication_classes = ()
            self.permission_classes = (IsAuthenticatedOrReadOnly,)

        return initialized_request

    def post(self, request):
        serializer = self.get_serializer(data=request.DATA)

        if serializer.is_valid():
            return Response(serializer.object)

        return ErrorResponse(serializer.errors)


class SearchAPIView(generics.ListAPIView):
    serializer_class = SearchSerializer
    permission_classes = ()
    authentication_classes = ()

    def get_queryset(self):
        search_by = self.request.QUERY_PARAMS.get('search_by')
        search_value = self.request.QUERY_PARAMS.get('search_value')
        sort_field = self.request.QUERY_PARAMS.get('sort_field')

        query = None

        if search_by != 'isbn_10' and search_by != 'isbn_13':
            field_specification = search_by + '__icontains'
            query = Book.objects.filter(**{
                field_specification: search_value})
        else:
            field_specification = search_by + '__iexact'
            query = Book.objects.filter(**{
                field_specification: search_value})

        if sort_field:
            if sort_field.lower() != 'price':
                query = query.order_by((sort_field.lower()))

        return query


class SearchAutoCompleteAPIView(generics.ListAPIView):
    serializer_class = BookSimpleSerializer
    permission_classes = ()
    authentication_classes = ()

    def get_queryset(self):
        search_by = self.request.QUERY_PARAMS.get('search_by')
        search_value = self.request.QUERY_PARAMS.get('search_value')

        query = None

        if search_by != 'isbn_10' and search_by != 'isbn_13':
            field_specification = search_by + '__icontains'
            query = Book.objects.filter(**{
                field_specification: search_value})
        else:
            field_specification = search_by + '__iexact'
            query = Book.objects.filter(**{
                field_specification: search_value})

        if query:
            return query
        else:
            wrapper = SearchWrapper()
            data = wrapper.search_isbndb_api(search_by, search_value)
            return json.loads(data)


class TopRequestedAPIView(generics.ListAPIView):
    model = Requested
    queryset = Requested.objects.order_by('-count')[:5]
    serializer_class = RequestedSerializer
    permission_classes = ()
    authentication_classes = ()


# Way to complicated and query hog
class TopRecommendedAPIView(generics.ListAPIView):
    model = Book
    serializer_class = BookSerializer

    def get_queryset(self):
        result_query = None
        viewed = Viewed.objects.filter(user=self.request.user)
        for v in viewed:
            result_query = chain(result_query, Book.objects.filter(
                Q(author__icontains=v.book.author) |
                Q(category__iexact=v.book.category) |
                Q(publisher__icontains=v.book.publisher)
            ).order_by('author', 'category', 'score', 'publisher)')[:5]
            )
        if result_query is None:
            return []
        return result_query

# No Paypal payments without being the clearing house
# class TopSellersAPIView(generics.ListAPIView):
#     model = Book
#     serializer_class = BookSerializer
#     permission_classes = ()
#     queryset = Requested.objects.order_by('-count')[:5]
