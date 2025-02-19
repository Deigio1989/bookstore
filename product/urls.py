from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .viewsets import ProductViewSet, CategoryViewSet

router = SimpleRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'categories', CategoryViewSet, basename='category')  # Registrar rota de Category

urlpatterns = [
    path('', include(router.urls)),
]

