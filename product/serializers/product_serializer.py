from rest_framework import serializers
from product.models import Product, Category
from product.serializers.category_serializer import CategorySerializer

class ProductSerializer(serializers.ModelSerializer):
    categories_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), write_only=True, many=True)
    category = CategorySerializer(many=True, required=False)  # Usando CategorySerializer aqui

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'active', 'categories_id', 'category']

    def create(self, validated_data):
        categories_data = validated_data.pop('categories_id')
        product = Product.objects.create(**validated_data)
        for category in categories_data:
            product.category.add(category)
        return product
