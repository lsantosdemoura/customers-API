import asyncio
import json
from collections import OrderedDict

from django.http import Http404
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from aiohttp import ClientSession

from core.models import Customer
from core.models import FavoriteList
from api.serializers import CustomerSerializer
from api.serializers import FavoriteListSerializer
from api import utils


class CustomerViewSet(viewsets.ViewSet):
    """
    API endpoint that allows customers to be viewed or edited.
    """
    permission_classes = (IsAuthenticated, )
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    responses = []

    def list(self, request):
        fields = ('name', 'email', 'url')
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True, context={'request': request}, fields=fields)
        return Response(serializer.data)

    def create(self, request):
        product_id = request.data.get('product_id')
        if product_id:
            product_id_status = utils.check_product_id(request.data.get('product_id'))
            # using false to make it explicit
            if product_id_status is False:
                return Response(
                    {"product_id": "This product does not exist."},
                    status.HTTP_400_BAD_REQUEST
                )

        fields = ('name', 'email', 'url')
        serializer = CustomerSerializer(data=request.data, context={'request': request}, fields=fields)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self, pk):
        try:
            return Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            raise Http404

    def get_data_response(self, serializer_data):
        all_product_ids = [p_id["product_id"] for p_id in serializer_data.get("favorites")]

        async def run(product_ids):
            url = "http://challenge-api.luizalabs.com/api/product/{}"
            tasks = []

            # Fetch all responses within one Client session,
            # keep connection alive for all requests.
            async with ClientSession() as session:
                for product_id in product_ids:
                    task = asyncio.ensure_future(utils.fetch(url.format(product_id), session))
                    tasks.append(task)

                self.responses = await asyncio.gather(*tasks)

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        future = asyncio.ensure_future(run(all_product_ids))
        loop.run_until_complete(future)

        needed_fields = ('id', 'title', 'image', 'price', 'reviewScore')

        def get_product_values(response):
            json_response = json.loads(response)
            product_fields = OrderedDict([(field, json_response.get(field)) for field in needed_fields])

            return product_fields

        all_products = [get_product_values(response) for response in self.responses]

        data_response = serializer_data
        def add_url(p_id, url):
            for product in all_products:
                if product['id'] == p_id:
                    product['url'] = url
                    product['product_id'] = p_id
                    product.move_to_end('product_id', last=False)

        urls_ids = [(favorite['product_id'], favorite['url']) for favorite in data_response['favorites']]
        for url_id in urls_ids:
            add_url(*url_id)

        for product in all_products:
            del product['id']

        data_response['favorites'] = all_products

        return data_response

    def retrieve(self, request, pk, format=None):
        fields = ('name', 'email', 'favorites')
        customer = self.get_object(pk)
        serializer = CustomerSerializer(customer, context={'request': request}, fields=fields)
        data_response = self.get_data_response(serializer_data=serializer.data)

        return Response(data_response)

    def partial_update(self, request, pk, format=None):
        favorites = request.data.get('favorites')
        product_id_statuses = [utils.check_product_id(product_status.get("product_id")) for product_status in favorites]

        if not any(product_id_statuses):
            return Response(
                {"product_id": "This product does not exist."},
                status.HTTP_400_BAD_REQUEST
            )

        fields = ('name', 'email', 'favorites')
        customer = self.get_object(pk)
        serializer = CustomerSerializer(customer, data=request.data, context={'request': request}, fields=fields)
        if serializer.is_valid():
            serializer.save()
            data_response = self.get_data_response(serializer_data=serializer.data)
            return Response(data_response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk, format=None):
        customer = self.get_object(pk)
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteListViewSet(viewsets.ViewSet):
    """
    API endpoint that allows products to be viewed or edited.
    """
    permission_classes = (IsAuthenticated, )
    queryset = FavoriteList.objects.all()
    serializer_class = FavoriteListSerializer

    def list(self, request):
        products = FavoriteList.objects.all()
        serializer = FavoriteListSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        product_id_status = utils.check_product_id(request.data.get('product_id'))
        # using false to make it explicit
        if product_id_status is False:
            return Response(
                {"product_id": "This product does not exist."},
                status.HTTP_400_BAD_REQUEST
            )
        serializer = FavoriteListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self, pk):
        try:
            return FavoriteList.objects.get(pk=pk)
        except FavoriteList.DoesNotExist:
            raise Http404

    def retrieve(self, request, pk, format=None):
        fields = ('product_id', 'customer', 'url')
        product = self.get_object(pk)
        serializer = FavoriteListSerializer(product, context={'request': request})
        return Response(serializer.data)

    def destroy(self, request, pk, format=None):
        product = self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
