from rest_framework.response import Response
from rest_framework import generics, filters

from . import serializers
from .models import User
from ..utils.response import ErrorResponse


class SigninAPIView(generics.CreateAPIView):
    throttle_classes = ()
    permission_classes = ()
    serializer_class = serializers.SigninSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.DATA)

        if serializer.is_valid():
            return Response(serializer.object)

        return ErrorResponse(serializer.errors)


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
            'exclude': ('email', 'created_at', 'modified_at', 'phone',
                        'address_1', 'address_2', 'country', 'city',
                        'state', 'zip', 'facebook_url', 'twitter_url',
                        'google_url', 'institution', 'department',
                        'description', 'logo', 'company_name', )
        })

        return serializer_class(*args, **kwargs)

    def filter_queryset(self, queryset):
        params = self.request.QUERY_PARAMS.get('search')

        if not params:
            return []

        users = User.active.exclude(pk=self.request.user.pk)
        queryset = super(UserAutoCompleteAPIView, self).filter_queryset(users)

        return queryset[:10]


class SignupAPIView(generics.CreateAPIView):
    throttle_classes = ()
    permission_classes = ()
    serializer_class = serializers.SignupSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.DATA)

        if serializer.is_valid():
            return Response(serializer.object)

        return ErrorResponse(serializer.errors)


class ChangePasswordAPIView(generics.UpdateAPIView):
    model = User
    serializer_class = serializers.ChangePasswordSerializer

    def put(self, request):
        serializer = self.serializer_class(
            data=request.DATA, instance=request.user)

        if serializer.is_valid():
            data = serializers.UserSettingsSerializer(serializer.object).data
            return Response(data)

        return ErrorResponse(serializer.errors)

    def get_object(self):
        return self.request.user


class ForgotPasswordAPIView(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = serializers.ForgotPasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.DATA)

        if serializer.is_valid():
            serializer.send_password_reset_email()
            return Response(serializer.data)

        return ErrorResponse(serializer.errors)


class ResetPasswordAPIView(generics.UpdateAPIView):
    model = User
    serializer_class = serializers.ResetPasswordSerializer

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.DATA)

        if serializer.is_valid():
            return Response(serializer.data)

        return ErrorResponse(serializer.errors)

    def get_object(self):
        return self.request.user


class CancelAccountAPIView(generics.UpdateAPIView):
    model = User
    authentication_classes = ()
    permission_classes = ()
    serializer_class = serializers.CancelAccountSerializer

    def put(self, request):
        serializer = self.serializer_class(
            data=request.DATA, instance=request.user)

        if serializer.is_valid():
            self.object = serializer.save()
            serializer.data['canceled'] = True
            return Response(serializer.data)

        return ErrorResponse(serializer.errors)

    def get_object(self):
        return self.request.user


class UserSettingsAPIView(generics.UpdateAPIView):
    model = User
    serializer_class = serializers.UserSettingsSerializer

    def put(self, request):
        serializers = self.serializer_class(
            data=request.DATA, instance=request.user)

        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)

    def get_object(self):
        return self.request.user