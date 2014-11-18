from rest_framework.viewsets import ModelViewSet

from .models import OrderItem
from .serializers import OrderItemSerializer
from .permissions import OrderItemPermission


class OrderItemViewSet(ModelViewSet):
    model = OrderItem
    serializer_class = OrderItemSerializer
    permission_classes = (OrderItemPermission, )

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
