import pytest

from core.models import Customer
from core.models import FavoriteList


@pytest.mark.django_db(transaction=True)
class TestModelsSetUp:
    @pytest.fixture
    def customer_name(self):
        name = 'Lucas'
        return name

    @pytest.fixture
    def customer_email(self):
        email = 'lucas@email.com'
        return email

    @pytest.fixture
    def test_customer(self, customer_name, customer_email):
        test_customer = Customer.objects.create(
            name=customer_name,
            email=customer_email,
        )
        return test_customer

    @pytest.fixture
    def product_id(self):
        product_id = "test-product-id"
        return product_id

    @pytest.fixture
    def test_favorite_list(self, test_customer, product_id):
        test_favorite_list = FavoriteList.objects.create(
            customer=test_customer,
            product_id=product_id,
        )
        return test_favorite_list


@pytest.mark.django_db(transaction=True)
class TestCustomers(TestModelsSetUp):

    def test_customer_instance(self, test_customer):
        assert isinstance(test_customer, Customer)

    def test_customer_get_name(self, test_customer, customer_name):
        assert test_customer.name == customer_name

    def test_customer_get_email(self, test_customer, customer_email):
        assert test_customer.email == customer_email

    def test_customer_str(self, test_customer, customer_name):
        assert test_customer.__str__() == customer_name


@pytest.mark.django_db(transaction=True)
class TestFavoriteList(TestModelsSetUp):

    @pytest.mark.django_db(transaction=True)
    def test_product_instance(self, test_favorite_list):
        pytestmark = pytest.mark.django_db
        assert isinstance(test_favorite_list, FavoriteList)

    @pytest.mark.django_db(transaction=True)
    def test_product_str(self, test_favorite_list, product_id):
        pytestmark = pytest.mark.django_db
        assert test_favorite_list.__str__() == product_id
