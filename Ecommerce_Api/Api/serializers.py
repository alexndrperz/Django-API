from rest_framework import serializers
from .models import Category, Product,Transacts
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group


class GroupsSerializer(serializers.Serializer): 

    class Meta:
        model = Group
        fields = ['id','name','users_count']
       

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['id'] = instance.id
        rep['name'] = instance.name
        rep['user_count'] = self.get_users_count(instance)
        return rep

    def get_users_count(self, obj):
        count = obj.user_set.count()
        return count 


class UserSerializer(serializers.ModelSerializer):
    group = serializers.SerializerMethodField()
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        print(validated_data)
        return super().create(validated_data)
    class Meta:
        model = get_user_model() 
        extra_kwargs = {'password':{'write_only':True}}
        fields = ['id','email','password','name','is_active','group']
    def get_group(self, obj):
        return list(obj.groups.values_list('name',flat=True))


class UserNestedSerializer(serializers.ModelSerializer):
    group= serializers.SerializerMethodField()

    class Meta:
        model= get_user_model()
        fields = ['id','name','is_active','group']

    def get_group(self, obj):
        return list(obj.groups.values_list('name',flat=True))


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()
    products = serializers.SerializerMethodField()
    class Meta:
        model = Category 
        fields =  ['id','nameCategory','product_count','products']

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


class ProductSerializer(serializers.ModelSerializer):
    category  = CategoryNestedSerializer(source="category_id")
    seller = UserNestedSerializer(source="seller_id")

    class Meta:
        model = Product
        fields = ['id','nameProduct','priceProduct','dateReleased','is_digital','active','category','seller']

class ProductCreatorSerializer(serializers.ModelSerializer):
    seller_id = serializers.ReadOnlyField()
    
    class Meta:
        model  = Product
        fields = ['id','nameProduct','priceProduct', 'active','category_id', 'seller_id']



# class SellerSerializer(serializers.ModelSerializer):
#     products = serializers.SerializerMethodField()

#     class Meta: 
#         model = Sellers
#         fields = ['id','nameSeller','lastNameSeller','registerDate', 'products']

#     def get_products(self, obj):
#         products = Product.objects.filter(seller_id=obj.id)
#         return ProductSerializer(products, many=True).data


# class SellerNestedSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Sellers
#         fields = '__all__'

class TransactProductNestedSerializer(serializers.ModelSerializer):
    seller = UserNestedSerializer(source='seller_id')

    class Meta:
        model = Product
        fields = ['id','nameProduct','priceProduct','dateReleased','active', 'seller']

class TransactsSerializer(serializers.ModelSerializer):
    product = TransactProductNestedSerializer()
    buyers = UserNestedSerializer()
    dateTransact = serializers.DateTimeField(format="%m/%d/%Y %I:%M:%S %p")
    
    class Meta:
        model  = Transacts 
        fields = ['id','dateTransact','product','buyers']






class AuthenticationSerializer(serializers.Serializer):
    email= serializers.EmailField()
    password = serializers.CharField(style={'input_type':'password'})

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
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