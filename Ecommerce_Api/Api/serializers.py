# from rest_framework import serializers
# from .models import Category, Product

# class ProductSerializer(serializers.ModelSerializer):
#     category_name = serializers.CharField(source='category_id.nameCategory')
    
#     class Meta:
#         model = Product
#         fields = ['id','nameProduct','priceProduct','active']

# class CategorySerializer(serializers.ModelSerializer):
#     products = ProductSerializer(many=True, read_only=True)
    
#     class Meta:
#         model = Category
#         fields = ['id', 'nameCategory', 'products']