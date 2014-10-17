from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Offer
from .serializers import OffersSerializer


class OffersViewSet(ModelViewSet):
    model = Offer
    serializer_class = OffersSerializer

    def initialize_request(self, request, *args, **kwargs):
        """
        Disable authentication and permissions for `create` action.
        """
        initialized_request = super(
            OffersViewSet, self).initialize_request(request, *args, **kwargs)

        user = request.user
        request_method = request.method.lower()
        action = self.action_map.get(request_method)

        if not user.is_authenticated() and (action == 'list' or action == 'retrieve'):
            self.authentication_classes = ()
            self.permission_classes = (IsAuthenticatedOrReadOnly,)

        return initialized_request
