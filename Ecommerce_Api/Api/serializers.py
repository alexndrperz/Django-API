from rest_framework import serializers
from .models import Category, Product, Buyers,Transacts, Sellers



class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()
    products = serializers.SerializerMethodField()
    class Meta:
        model = Category 
        fields =  ['id','nameCategory','product_count','products']

    def get_product_count(self,obj):
        count = obj.products_quantity
        return count
    
    def get_products(self, obj):
        products = Product.objects.filter(category_id=obj.id)
        return ProductSerializer(products, many=True).data

class CategoryNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','nameCategory']

class BuyerSerializer(serializers.ModelSerializer):
    dateRegister = serializers.DateTimeField(format="%m/%d/%Y %I:%M:%S %p")
    
    class Meta:
        model = Buyers
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category  = CategoryNestedSerializer(source="category_id")
    
    class Meta:
        model = Product
        fields = ['id','nameProduct','priceProduct','dateReleased','active','category']

class TransactBuyersNestedSerializer(serializers.ModelSerializer):
    dateRegister = serializers.DateTimeField(format="%m/%d/%Y %I:%M:%S %p")
    class Meta:
        model = Buyers
        fields = '__all__'

class SellerSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta: 
        model = Sellers
        fields = ['id','nameSeller','lastNameSeller','registerDate', 'products']

    def get_products(self, obj):
        products = Product.objects.filter(seller_id=obj.id)
        return ProductSerializer(products, many=True).data


class SellerNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sellers
        fields = '__all__'

class TransactProductNestedSerializer(serializers.ModelSerializer):
    seller = SellerNestedSerializer(source='seller_id')

    class Meta:
        model = Product
        fields = ['id','nameProduct','priceProduct','dateReleased','active','seller']

class TransactsSerializer(serializers.ModelSerializer):
    product = TransactProductNestedSerializer()
    buyers = TransactBuyersNestedSerializer()
    dateTransact = serializers.DateTimeField(format="%m/%d/%Y %I:%M:%S %p")
    
    class Meta:
        model  = Transacts 
        fields = ['id','dateTransact','product','buyers']


    



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