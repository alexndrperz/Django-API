from django.forms import ValidationError
from rest_framework import serializers,exceptions
from .models import Category, Product,Transacts,User,InvitationCodes
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from .utils import services as uti
import random
import string

dateFormat = serializers.DateTimeField(format="%d/%m/%Y %I:%M:%S %p",required=False)

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
    last_login = serializers.DateTimeField(format="%d/%m/%Y %I:%M:%S %p")
    
    class Meta:
        model = get_user_model() 
        extra_kwargs = {'password':{'write_only':True}}
        fields = ['id','email','password','name','is_active','group', 'last_login']

 
    def get_group(self, obj):
        print(obj)
        return list(obj.groups.values_list('name',flat=True))


    
class InvitationCodesSerializer(serializers.ModelSerializer):
    expire_date = dateFormat
    created_at = serializers.DateTimeField(format="%d/%m/%Y %I:%M:%S %p",required=False)
    class Meta:
        model = InvitationCodes
        fields=['invitationCodes','description','is_used','is_expired','created_at','expire_date']

class UserCreatorSerializer(serializers.ModelSerializer):
    group_names = serializers.ListField(child=serializers.CharField(), required=False)
    invitation_code = serializers.CharField()
    class Meta:
        model = get_user_model() 
        fields = ['id','email','password','name','is_active','group_names', 'invitation_code']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        group_name = validated_data.pop('group_names', None)
        invitation_code = validated_data.pop('invitation_code',None)
        try:
            if invitation_code:
                print("ss")
                invitationObj = InvitationCodes.objects.get(invitationCodes=invitation_code)    
                print(invitationObj)
                serializer = InvitationCodesSerializer(instance=invitationObj, data={'is_used':True})
                if serializer.is_valid():
                    serializer.save()
                    print("as")
        except:
            raise exceptions.ValidationError("No se ha encontrado su codigo de invitacion")
            
        validated_data['password'] = make_password(validated_data['password'])
        not_found_groups = []
        groups = []
        if group_name: 
            for group_n in group_name:
                try:
                    group = Group.objects.get(name=group_n)
                    groups.append(group)
                except Group.DoesNotExist:
                    not_found_groups.append(group_n)

            if not_found_groups:
                message = f"Groups {', '.join(not_found_groups)} not found"
                raise serializers.ValidationError(message, code=400)


            user = User.objects.create_user(**validated_data)
            for group in groups:
                user.groups.add(group)
        user = User.objects.create_user(**validated_data)
        return user

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
            email=email,
            password = password
        )  

        if not user:
            raise serializers.ValidationError('Sus credenciales han sido incorrectas', code=401)

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