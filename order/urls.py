from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .viewsets import OrderViewSet

router = SimpleRouter()
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
]
