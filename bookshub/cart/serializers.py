from rest_framework import serializers

from .models import OrderItem


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ('id', 'offer', 'quantity', 'is_purchased', 'purchased_date')

    def validate(self, attrs):
        print attrs
        quantity = attrs['quantity']
        offer = attrs['offer']
        buyer = self.context['request'].user

        if buyer == offer.owner:
            message = 'Invalid action, you can not buy your own book.'
            raise serializers.ValidationError(message)

        if quantity > offer.quantity:
            message = 'The quantity entered is not valid.'
            raise serializers.ValidationError(message)

        return attrs

    def save_object(self, obj, **kwargs):
        obj.user = self.context['request'].user
        super(OrderItemSerializer, self).save_object(obj, **kwargs)
