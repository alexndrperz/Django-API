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
    shares_count = serializers.SerializerMethodField()
    purchases_count = serializers.SerializerMethodField()
    
    class Meta:
        model = get_user_model() 
        extra_kwargs = {'password':{'write_only':True}}
        fields = ['id','email','password','name','is_active','group', 'last_login', 'shares_count', 'purchases_count']

    def get_shares_count(self, obj):
        return obj.shares_count

    def get_purchases_count(self, obj):
        return obj.purchases_count

 
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
    group_names = serializers.ListField(child=serializers.CharField(), read_only=True)
    invitation_code = serializers.CharField()
    class Meta:
        model = get_user_model() 
        fields = ['id','email','password','name','is_active','group_names', 'invitation_code']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        group_name = validated_data.pop('group_names', ["buyers"])
        invitation_code = validated_data.pop('invitation_code',None)
        message = ""
        try:
            if invitation_code:
                invitationObj = InvitationCodes.objects.get(invitationCodes=invitation_code)
        except:
            message = "No se ha encontrado su codigo de invitacion"
            raise serializer.ValidationError({"message":message})    
        if invitationObj.is_used == False and invitationObj.is_expired == False:
            serializer = InvitationCodesSerializer(instance=invitationObj, data={'is_used':True})
            if serializer.is_valid():
                serializer.save()
        else:
            message = "Code de invitacion previamente usado o expirado"
            raise serializers.ValidationError({"message":message})
        group = Group.objects.get(name=group_name[0]) 
        validated_data['password'] = make_password(validated_data['password'])
        user = User.objects.create_user(**validated_data)
        user.groups.add(group)
        return user


        # not_found_groups = []
        # groups = []
        # if group_name: 
        #     for group_n in group_name:
        #         try:
        #             group = Group.objects.get(name=group_n)
        #             groups.append(group)
        #         except Group.DoesNotExist:
        #             not_found_groups.append(group_n)

        #     if not_found_groups:
        #         message = f"Groups {', '.join(not_found_groups)} not found"
        #         raise serializers.ValidationError(message, code=400)
        #     validated_data['password'] = make_password(validated_data['password'])
        #     user = User.objects.create_user(**validated_data)
        #     for group in groups:
        #         user.groups.add(group)
        # return user

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
        products = Product.objects.filter(category_id=obj.id, active=True)
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
    seller = UserNestedSerializer(read_only=True)
    category = CategoryNestedSerializer(read_only=True)
    category_id = serializers.IntegerField(required=True, write_only=True)
    price = serializers.SerializerMethodField()
    priceProduct = serializers.DecimalField(max_digits=10,decimal_places=2,write_only=True)

    def get_price(self, obj):
        print(obj.priceProduct)
        return f"{obj.priceProduct} USD"

    class Meta:
        model = Product
        fields = [
                    'id',
                    'nameProduct',
                    'price',
                    'dateReleased',
                    'is_digital',
                    'active',
                    'seller', 
                    'category',
                    'category_id',
                    'priceProduct'
                ]


    def create(self, validated_data):
        request = self.context.get('request')
        category_id = validated_data.pop('category_id', None)
        price = validated_data.pop('priceProduct', None)
        validated_data.pop('seller_id')
        print("asdas")
        seller = User.objects.get(id=request.user.id)
        try:
            category = Category.objects.get(id=category_id)
        except:
            raise exceptions.ValidationError("La categoria especificada no existe")
        product = Product.objects.create(seller=seller, priceProduct=price, category=category, **validated_data)
        return product

    def update(self, instance, validated_data):
        userValidation= self.context.get('userPermision')
        if userValidation['IsChecker'] and not userValidation['IsAdmin'] and any( key != 'active' for key in validated_data.keys()):
            raise serializers.ValidationError({"message":"No puede editar esto"}) 
        return super().update(instance, validated_data)

    def to_internal_value(self, data):
            valid_fields = set(self.fields.keys())
            input_fields = set(data.keys())
            userValidation= self.context.get('userPermision') 
            print(valid_fields)
            print(input_fields)
            
            if 'id' in data:
                raise serializers.ValidationError({"Parametro no autorizado":['id']})

            if userValidation['IsSeller'] and not userValidation['IsChecker'] and not userValidation['IsAdmin'] and 'active' in input_fields:
                raise serializers.ValidationError({'message': 'No es checker'})
            
            if not input_fields.issubset(valid_fields):
                invalid_fields = input_fields - valid_fields
                INVList = list(invalid_fields)
                print(INVList)
                raise serializers.ValidationError({"Parametros Invalidos":INVList})
            return super().to_internal_value(data)



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
    product_id = serializers.IntegerField(write_only=True)
    product = TransactProductNestedSerializer(read_only=True)
    buyers = UserNestedSerializer(read_only=True)
    dateTransact = serializers.DateTimeField(format="%m/%d/%Y %I:%M:%S %p", read_only=True)
    
    class Meta:
        model  = Transacts 
        fields = ['id','dateTransact','product','buyers', 'product_id']

    def create(self, validated_data):
        print(validated_data)
        product_id = validated_data.pop('product_id', None)
        request = self.context.get('request')
        buyer_id= request.user.id
        buyers = User.objects.get(id=buyer_id)
        print(buyers)
        products = Product.objects.get(id=product_id)
        transact = Transacts.objects.create(product=products,buyers=buyers, **validated_data)
        return transact






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