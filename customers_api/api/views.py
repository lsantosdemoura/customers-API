from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.mixins import RetrieveModelMixin

from core.models import Customer
from core.models import FavoriteList
from api.serializers import CustomerSerializer
from api.serializers import FavoriteListSerializer


class CustomerViewSet(viewsets.ViewSet):
    """
    API endpoint that allows customers to be viewed or edited.
    """
    permission_classes = (IsAuthenticated, )
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def list(self, request):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self, pk):
        try:
            return Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            raise Http404

    def retrieve(self, request, pk, format=None):
        customer = self.get_object(pk)
        serializer = CustomerSerializer(customer, context={'request': request})
        return Response(serializer.data)

    def partial_update(self, request, pk, format=None):
        customer = self.get_object(pk)
        serializer = CustomerSerializer(customer, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk, format=None):
        customer = self.get_object(pk)
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteListViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed or edited.
    """
    permission_classes = (IsAuthenticated, )
    queryset = FavoriteList.objects.all()
    serializer_class = FavoriteListSerializer

    # def list(self, request):
    #     products = FavoriteList.objects.all()
    #     serializer = FavoriteListSerializer(products, many=True, context={'request': request})
    #     return Response(serializer.data)
    #
    # def create(self, request):
    #     # email = request.data["customer_email"]
    #     # customer = Customer.objects.get(email=email)
    #
    #     serializer = FavoriteListSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # def get_object(self, pk):
    #     try:
    #         return FavoriteList.objects.get(pk=pk)
    #     except FavoriteList.DoesNotExist:
    #         raise Http404
    #
    # def retrieve(self, request, pk, format=None):
    #     product = self.get_object(pk)
    #     serializer = FavoriteListSerializer(product)
    #     return Response(serializer.data)
    #
    # def partial_update(self, request, pk, format=None):
    #     product = self.get_object(pk)
    #     serializer = FavoriteListSerializer(product, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # def destroy(self, request, pk, format=None):
    #     product = self.get_object(pk)
    #     product.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
