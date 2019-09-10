from rest_framework import serializers

from core.models import Customer
from core.models import FavoriteList


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    favorites = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='favoritelist-detail')

    class Meta:
        model = Customer
        fields = ('name', 'email', 'favorites')


class FavoriteListSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = FavoriteList
        fields = ('customer', 'product_id')
