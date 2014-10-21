from rest_framework.viewsets import ModelViewSet

from .models import Cart
from .serializers import CartSerializer


class CartViewSet(ModelViewSet):
    model = Cart
    serializer_class = CartSerializer
