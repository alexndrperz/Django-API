from rest_framework import serializers
from .models import Category, Product, Buyers,Transacts, Sellers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password



class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()
    products = serializers.SerializerMethodField()
    class Meta:
        model = Category 
        fields =  ['id','nameCategory','product_count','products']

    prop = 0

    def get_product_count(self,obj):
        count = obj.products_quantity
        self.prop = count
        return count
    
    def get_products(self, obj):
        if obj.products_quantity == 0:
            products = "N/A"
            return products
        products = Product.objects.filter(category_id=obj.id)
        return ProductSerializer(products, many=True).data

class CategoryWithoutProductsSerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()
    class Meta:
        model = Category 
        fields =  ['id','nameCategory','product_count']
        
        def get_product_count(self,obj):
            count = obj.products_quantity
            return count

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

class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        print(validated_data)
        return super().create(validated_data)

    class Meta:
        model = get_user_model() 
        extra_kwargs = {'password':{'write_only':True}}
        fields = ['id','email','password','name','is_active','groups']




class AuthenticationSerializer(serializers.Serializer):
    email= serializers.EmailField()
    password = serializers.CharField(style={'input_type':'password'})

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        print(password)
        user = authenticate(
            request= self.context.get('request'),
            username=email,
            password = password
        )  

        if not user:
            raise serializers.ValidationError('Pa fuera jakel', code='authorization')

        data['user'] = user 
        return data
    



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