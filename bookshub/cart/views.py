from django.core.mail import EmailMessage

from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import OrderItem
from .serializers import OrderItemSerializer
from .permissions import OrderItemPermission

from ..utils.response import ErrorResponse


class OrderItemViewSet(ModelViewSet):
    model = OrderItem
    serializer_class = OrderItemSerializer
    permission_classes = (OrderItemPermission, )

    def get_queryset(self):
        return self.model.objects.filter(
            user=self.request.user, is_purchased=False)


class BuyItemsInCartView(APIView):

    def post(self, request):
        cart_items = OrderItem.objects.filter(
            user=request.user, is_purchased=False)

        if len(cart_items) > 0:
            for item in cart_items:
                item.is_purchased = True

                item.save()

                email = EmailMessage(to=[request.user.email], from_email=None)

                email.template_name = "bought-item"
                email.use_template_subject = True
                email.use_template_from = True

                email.global_merge_vars = {
                    "BUYER_NAME": request.user.get_full_name(),
                    "BUYER_EMAIL": request.user.email,
                }

                email.send(fail_silently=False)
            return Response({"success": True})
        return ErrorResponse({"message": "cart must not be empty to checkout."})
