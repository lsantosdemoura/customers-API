from collections import OrderedDict

from rest_framework import serializers

from core.models import Customer
from core.models import FavoriteList


class DynamicFieldsModelSerializer(serializers.HyperlinkedModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

            ordered_fields = OrderedDict.fromkeys(fields)
            for key in ordered_fields:
                ordered_fields[key] = self.fields[key]
            self.fields = ordered_fields


class FavoriteListSerializer(serializers.HyperlinkedModelSerializer):
    customer_email = serializers.CharField(required=False, max_length=200)
    customer = serializers.SerializerMethodField()

    class Meta:
        model = FavoriteList
        fields = '__all__'

    def create(self, validated_data):
        customer_email = validated_data.get('customer_email')
        customer = Customer.objects.get(email=customer_email)
        product_id = validated_data.get('product_id')
        # get or create for avoid repeating a product in list
        favorite = FavoriteList.objects.get_or_create(customer=customer, product_id=product_id)

        return favorite

    def get_customer(self, obj):
        return obj.customer.email


class CustomerSerializer(DynamicFieldsModelSerializer):
    favorites = FavoriteListSerializer(many=True, required=False)

    class Meta:
        model = Customer
        fields = '__all__'

    def create(self, validated_data):
        favorites_data = validated_data.pop('favorites', [])
        customer = Customer.objects.create(**validated_data)
        for favorite_data in favorites_data:
            FavoriteList.objects.create(customer=customer, **favorite_data)

        return customer

    def update(self, instance, validated_data):
        favorites_data = validated_data.pop('favorites')
        instance.email = validated_data.get('email')
        instance.name = validated_data.get('name')
        instance.save()
        for favorite_data in favorites_data:
            product_id = favorite_data.get('product_id')
            instance.favorites.get_or_create(product_id=product_id)
            instance.save()

        return instance
