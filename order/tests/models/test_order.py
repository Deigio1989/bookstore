import pytest

from order.factories import OrderFactory
from order.factories import UserFactory

@pytest.fixture
def order():
    return OrderFactory(user = UserFactory(username = "test"))

@pytest.mark.django_db
def test_create_order(order):
    assert order.user.username == 'test'