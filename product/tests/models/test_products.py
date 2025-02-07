import pytest

from product.factories import ProductFactory

@pytest.fixture
def product():
    return ProductFactory(title='pytest with factory')

@pytest.mark.django_db
def test_create_order(product):
    assert product.title == 'pytest with factory'