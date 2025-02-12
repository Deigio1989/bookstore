from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .viewsets import ProductViewSet

router = SimpleRouter()
router.register(r'', ProductViewSet, basename='product')  # Registra a rota sem 'products'

urlpatterns = [
    path('', include(router.urls)),
]
