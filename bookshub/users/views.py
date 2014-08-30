from rest_framework.response import Response
from rest_framework import generics, filters

from . import serializers
from .models import User


class SigninAPIView(generics.CreateAPIView):
    throttle_classes = ()
    permission_classes = ()
    serializer_class = serializers.SigninSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.DATA)

        if serializer.is_valid():
            return Response(serializer.object)

        return Response(serializer.errors)


class UserAutoCompleteAPIView(generics.ListAPIView):
    model = User
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^username', '^first_name', '^last_name')
    serializer_class = serializers.UserSimpleSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        context = self.get_serializer_context()

        kwargs.update({
            'context': context,
            'exclude': ('username', 'created_at', 'modified_at')
        })

        return serializer_class(*args, **kwargs)

    def filter_queryset(self, queryset):
        params = self.request.QUERY_PARAMS.get('search')

        if not params:
            return []

        users = User.active.exclude(pk=self.request.user.pk)
        queryset = super(UserAutoCompleteAPIView, self).filter_queryset(users)

        return queryset[:10]


class SingupAPIView(generics.CreateAPIView):
    throttle_classes = ()
    permission_classes = ()
    serializer_class = serializers.SignupSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.DATA)

        if serializer.is_valid():
            return Response(serializer.object)

        return Response(serializer.errors)
