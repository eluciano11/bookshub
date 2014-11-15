from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Offer, Image
from .serializers import OfferSerializer, OfferImageSerializer
from .permissions import ImagePermission


class OfferViewSet(ModelViewSet):
    model = Offer
    serializer_class = OfferSerializer
    filter_fields = ('owner', )

    def initialize_request(self, request, *args, **kwargs):
        """
        Disable authentication and permissions for `list or retrieve` action.
        """
        initialized_request = super(
            OfferViewSet, self).initialize_request(request, *args, **kwargs)

        user = request.user
        request_method = request.method.lower()
        action = self.action_map.get(request_method)

        if not user.is_authenticated() and\
                (action == 'list' or action == 'retrieve'):
            self.authentication_classes = ()
            self.permission_classes = (IsAuthenticatedOrReadOnly,)

        return initialized_request


class OfferImageViewSet(ModelViewSet):
    model = Image
    serializer_class = OfferImageSerializer
    permission_classes = (ImagePermission, )

    def initialize_request(self, request, *args, **kwargs):
        """
        Disable authentication and permissions for `list or retrieve` action.
        """
        initialized_request = super(
            OfferViewSet, self).initialize_request(request, *args, **kwargs)

        user = request.user
        request_method = request.method.lower()
        action = self.action_map.get(request_method)

        if not user.is_authenticated() and\
                (action == 'list' or action == 'retrieve'):
            self.authentication_classes = ()
            self.permission_classes = (IsAuthenticatedOrReadOnly,)

        return initialized_request

    def get_queryset(self):
        return Image.objects.filter(
            book=self.kwargs['id'], book__owner=self.request.user)

    def pre_save(self, obj, *args, **kwargs):
        obj.book_id = self.kwargs['id']
