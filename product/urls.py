from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .viewsets import ProductViewSet, CategoryViewSet

router = SimpleRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'category', CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
]
