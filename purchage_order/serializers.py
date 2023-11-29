from purchage_order.models import Purchage_Order
from rest_framework import serializers
from vendors.serializers import VendorsSerializers

class PurchageOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchage_Order
        fields = ['items','vendor_id','order_date','delivery_date', 'quantity','po_number','status','vendor', 'quality_rating']
        extra_kwargs = {
            'order_date': {'required': False},
            'delivery_date': {'required': False},
            'quantity': {'required': False},
            'po_number': {'required': False},
            'vendor': {'required': False},
            'status': {'required': False},
            'quality_rating': {'required': False},

        }

    def update(self, instance, validated_data):
        instance.items = validated_data.get('items', instance.items)
        instance.vendor_id = validated_data.get('vendor_id', instance.vendor_id)
        instance.order_date = validated_data.get('order_date', instance.order_date)
        instance.delivery_date = validated_data.get('delivery_date', instance.delivery_date)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.po_number = validated_data.get('po_number', instance.po_number)
        instance.status = validated_data.get('status', instance.status)
        instance.quality_rating = validated_data.get('quality_rating', instance.quality_rating)
        instance.save()
        return instance

