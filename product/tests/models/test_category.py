import pytest

from product.factories import CategoryFactory


@pytest.fixture
def category():
    return CategoryFactory(title="pytest with factory")


@pytest.mark.django_db
def test_create_category(category):
    assert category.title == "pytest with factory"
