from rest_framework import serializers

from vendors.models import  Vendors

class VendorsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Vendors
        fields = ['name', 'contact_number', 'address',]

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.contact_number = validated_data.get('contact_number', instance.contact_number)
        instance.address = validated_data.get('address', instance.address)
        instance.save()

        return instance



