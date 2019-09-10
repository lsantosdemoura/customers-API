import json

from django.urls import reverse
from rest_framework import status
import pytest

from core.models import Customer
from core.models import FavoriteList
from api.serializers import CustomerSerializer


@pytest.mark.django_db(transaction=True)
class TestCustomerViews:
    @pytest.fixture
    def customer_1(self):
        customer_1 = Customer.objects.create(
            name="test1",
            email="test1@test.com",
        )
        return customer_1

    @pytest.fixture
    def customer_2(self):
        customer_2 = Customer.objects.create(
            name="test2",
            email="test2@test.com",
        )
        return customer_2
