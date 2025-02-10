from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .viewsets import ProductViewSet

router = SimpleRouter()
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
]
