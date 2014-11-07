from rest_framework.response import Response
from rest_framework import generics, filters
from rest_framework.viewsets import ModelViewSet

from . import serializers
from .models import User, Review
from ..utils.response import ErrorResponse


class SigninAPIView(generics.CreateAPIView):
    serializer_class = serializers.SigninSerializer
    throttle_classes = ()
    permission_classes = ()
    authentication_classes = ()

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
    authentication_classes = ()

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
    serializer_class = serializers.SignupSerializer
    throttle_classes = ()
    permission_classes = ()
    authentication_classes = ()

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


class ResetPasswordAPIView(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = serializers.ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.DATA)

        if serializer.is_valid():
            return Response(serializer.object)

        return ErrorResponse(serializer.errors)


class CancelAccountAPIView(generics.UpdateAPIView):
    model = User
    serializer_class = serializers.CancelAccountSerializer

    def put(self, request):
        serializer = self.serializer_class(
            data=request.DATA, instance=request.user)

        if serializer.is_valid():
            self.object = serializer.save()
            serializer.data['canceled'] = True
            return Response(serializer.data)

        return ErrorResponse(serializer.errors)


class UserSettingsAPIView(generics.UpdateAPIView, generics.RetrieveAPIView):
    model = User
    serializer_class = serializers.UserSettingsSerializer

    def put(self, request):
        serializer = self.serializer_class(
            data=request.DATA, instance=request.user)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return ErrorResponse(serializer.errors)

    def get_object(self):
        return self.request.user


class UserReviewViewSet(ModelViewSet):
    model = Review
    serializer_class = serializers.UserReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(owner=self.kwargs['user_id'])

    def initialize_request(self, request, *args, **kwargs):
        """
        Disable authentication and permissions for `list` action.
        """
        initialized_request = super(
            UserReviewViewSet, self).initialize_request(
                request, *args, **kwargs)

        user = request.user
        request_method = request.method.lower()
        action = self.action_map.get(request_method)

        if not user.is_authenticated() and\
                (action == 'list' or action == 'retrieve'):
            self.authentication_classes = ()
            self.permission_classes = ()

        return initialized_request

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        context = self.get_serializer_context()

        if self.request.method != 'GET':
            kwargs.update({
                'context': context,
                'exclude': ('created_by', 'owner')
            })

        return serializer_class(*args, **kwargs)


class UserProfileAPIView(generics.RetrieveAPIView):
    model = User
    serializer_class = serializers.UserSimpleSerializer
    authentication_classes = ()
    permission_classes = ()
    lookup_url_kwarg = 'id'
