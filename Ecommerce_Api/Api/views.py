from django.views import View
from django.http import response
from rest_framework import viewsets,permissions, authentication,mixins, exceptions
from rest_framework.permissions import IsAuthenticated
from django.http.response import JsonResponse 
from .authentications import IsAdmin, IsSeller, IsChecker, IsBuyer, IsGroupAccepted
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import  ObtainAuthToken
from rest_framework.authtoken.models import  Token
from django.contrib.auth.models import Group
from django.db.models import Q
from datetime import datetime, timedelta
from django.core import serializers
from rest_framework.views import APIView
from .models import Product,Category,Transacts,User,InvitationCodes
from .serializers import (TransactsSerializer, 
                          CategorySerializer,
                          CategoryWithoutProductsSerializer, 
                          ProductSerializer,
                          ProductCreatorSerializer,
                          UserSerializer,
                          UserCreatorSerializer,
                          UserNestedSerializer,
                          InvitationCodesSerializer,
                          AuthenticationSerializer,
                          GroupsSerializer)

def format_data(data=None, nameClass=None, code=200):
    status = 0
    if data==None and nameClass==None and code==200:
        return "No hay nada en la funcion"
    if code ==500:
        return {'message':'Ha habido un error en el servidor', 'status':code}
    if (len(data) > 0):
        result = {
            'success':True,
            nameClass:data,
            'status':code
        }
    else: 
        result = {
            'success':False,
            'message': f'No hay {nameClass} en la BD',
            'status':404
        }
    return result

def hasOrNotPermission(clss, request, view,obj=None,authClass=None, oneObj=False):
    if authClass != None:
        if oneObj== False:
            userComp = True if authClass.has_permission(clss, request, view) else False

        else:
            userComp = True if authClass.has_object_permission(clss, request,view,obj) else False
    return userComp



def validate_credentials(request,userProperty=None,groups=[],is_one_item=False, is_limited=False):
    if request.user.is_authenticated ==  False:
       return {'success':False,'status':401, 'message':'No esta autorizado'}
    validator = validate_group(request.user, ['administrator','sellers', 'checkers','buyers'])
    if validator == False and request.user.is_superuser == False:
        return {'success':False,'status':403}
    if is_limited:
            return {'success':True, 'userid':request.user.id}
    if is_one_item and is_limited:
        if validate_group(request.user, groups):
            if userProperty.id != request.user.id:
                return {'success':False,'status':403}


def validate_group(user, groups):
    if list(user.groups.values_list('name',flat=True)) == []:
        return None
    if list(user.groups.values_list('name',flat=True))[0] not in groups:
        return False
    else:
        return True


class ProductView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated,IsGroupAccepted]

    # GET all Products (with restrictions for sellers)
    def nested_list_products(self, request):
        user_products= request.GET.get('userProducts','false')
        if user_products == 'true':
            products = Product.objects.filter(seller_id=request.user.id, active=True)
            print("filtrado")
        elif user_products == 'false':
            products = Product.objects.all()
        else:
            return JsonResponse({"Message":"Not Found"}, status=400)
        serializer= ProductSerializer(products, many=True)
        return JsonResponse(serializer.data, status=200,safe=False)
    
    # GET just one product (Also with restricctions)
    def get_product(self, request, *args, **kwargs):
        instance = self.get_object()
        permission = hasOrNotPermission(self, request, self.__class__,obj=instance,oneObj=True,authClass=IsSeller)
        if not permission: 
            return JsonResponse({'success':False, 'message':'No ha vendido este producto'}, status=404)
        
        serializer = self.get_serializer(instance)
        return JsonResponse(serializer.data,status=200)
    
    # GET Digital Products (Checkers)
    def get_digital_products(self, request):
        checkersComp = hasOrNotPermission(self,request, self.__class__,authClass=IsChecker)
        adminsComp = hasOrNotPermission(self,request, self.__class__, authClass=IsAdmin)
        if checkersComp or adminsComp:
            products = Product.objects.filter(is_digital=True)
            serializer = ProductSerializer(products, many=True)
            return JsonResponse(serializer.data, status=200, safe=False)
        else: 
            return JsonResponse({"message":"No tienes permiso"}, status=401)
    
    # GET Last Products
    def get_last_products(self, request):
        now = datetime.now()
        start_time= now-timedelta(hours=24)
        products = Product.objects.filter(Q(dateReleased__gte=start_time))
        print(products)
        return 

    # POST a new product (Taking Seller id)
    def post_product(self,request):
        if request.user.is_authenticated ==  False:
            return JsonResponse({'success':False,'message':'No esta autenticado'}, status=401)
        validator = validate_group(request.user, ['administrator','sellers', 'checkers'])
        if validator == False and request.user.is_superuser == False:
            return JsonResponse({'success':False,'message':'No esta autorizado'}, status=403)
        serializer = ProductCreatorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = self.perform_create(serializer)
        serializerResp = ProductSerializer(obj)
        self.get_success_headers(serializer.data)
        return JsonResponse(serializerResp.data, status=200)
    
    # PUT a product created by a seller
    def update_product(self, request,*args, **kwargs):
        try:
            instance = self.get_object()
            if request.user.is_authenticated ==  False:
                return JsonResponse({'success':False,'message':'No esta autenticado'}, status=401)
            validator = validate_group(request.user, ['administrator','sellers', 'checkers'])
            if validator == False and request.user.is_superuser == False:
                return JsonResponse({'success':False,'message':'No esta autorizado'}, status=403)
            if validate_group(request.user, ['sellers']):
                if instance.seller_id.id != request.user.id:
                    return JsonResponse({'success':False, 'message':'No ha vendido este producto'}, status=404)
            
            serializer = self.get_serializer(instance,data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            fields = list(serializer.get_fields().keys())
            for key in request.data.keys():
                if key not in fields:
                    print(f"{key} no existe")
                    raise exceptions.ValidationError
        except response.Http404:
            return JsonResponse({'message':'No se encuentra el producto', 'status':404}, status=404)
        except exceptions.UnsupportedMediaType as e:
            return JsonResponse({'message':'El formato de su request no es valido', 'status':400}, status=400)
        except exceptions.ValidationError as e:
            return JsonResponse({'message':'Ha dejado uno o mas campos requeridos vacios', 'status':400}, status=400)
        except Exception as e:
            print(e)
            dicc = format_data(code=500)
            return JsonResponse(dicc, status=dicc['status'])
        self.perform_update(serializer)
        return JsonResponse({'message':'El campo ha sido actualizado', 'status':200}, status=200)

    # DELETE Product (with restrictions)
    def delete_product(self, request, *args, **kwargs):
        try:
            if request.user.is_authenticated ==  False:
                return JsonResponse({'success':False,'message':'No esta autenticado'}, status=401)
            validator = validate_group(request.user, ['administrator','sellers', 'checkers'])
            instance = self.get_object()
            if validator == False and request.user.is_superuser == False:
                return JsonResponse({'success':False,'message':'No esta autorizado'}, status=403)
            if validate_group(request.user, ['sellers']):
                if instance.seller_id.id != request.user.id:
                    return JsonResponse({'success':False, 'message':'No ha vendido este producto'}, status=403)
            instance= self.get_object()
            self.perform_destroy(instance)
            return JsonResponse({"Success":True, "message":"El producto fue borrado correctamente"}, status=200)
        except response.Http404 as e:
            return JsonResponse({"message":"No existe este producto"}, status=404)
        except Exception as e:
            print(e)
            print(type(e))
            return JsonResponse({}, status=500)

    # Overrides
    def perform_create(self, serializer):
        obj = serializer.save(seller_id=self.request.user)
        return obj

class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = [authentication.TokenAuthentication]

    #GET all Categories
    def nested_list_categories(self, request):
        try: 
            if request.user.is_authenticated == False:
                return JsonResponse({'message':'No autorizado'}, status=401)
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
            dicc = format_data(serializer.data, 'categorias')
            return JsonResponse(dicc, status=dicc['status'])   
        except Exception as e:
            dicc=format_data(code=500)
            print(e)
            return JsonResponse(dicc, status=dicc['status'])

    # GET one Category 
    def get_category(self, request, *args,**kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return JsonResponse(serializer.data, status=200)
        except response.Http404:
            return JsonResponse({'message':'No se encuentra la categoria',  'status':404}, status=404)
        except Exception as e: 
            print(type(e))
            return JsonResponse({'message':'Error'}, status=500)
        
    # POST One category
    def post_category(self, request):
        try:
            try: 
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception = True)
            except exceptions.UnsupportedMediaType as e:
                return JsonResponse({'message':'El formato de su request no es valido', 'status':400}, status=400)
            except exceptions.ValidationError as e:
                return JsonResponse({'message':e.detail, 'status':400}, status=400)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return JsonResponse(serializer.data, status=201, headers=headers)
        except Exception as e:
            dicc = format_data(code=500)
            return JsonResponse(dicc, status=dicc['status'])
    
    # PUT Instance
    def update_category(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
        except response.Http404:
            return JsonResponse({'message':'No se encuentra la categoria', 'status':404}, status=404)
        except exceptions.UnsupportedMediaType as e:
            return JsonResponse({'message':'El formato de su request no es valido', 'status':400}, status=400)
        except exceptions.ValidationError as e:
            return JsonResponse({'message':'Ha dejado uno o mas campos requeridos vacios', 'status':400}, status=400)
        except Exception as e:
            print(e)
            dicc = format_data(code=500)
            return JsonResponse(dicc, status=dicc['status'])
        self.perform_update(serializer)
        return JsonResponse({'message':'El campo ha sido actualizado', 'status':200}, status=200)

    # DELETE Category
    def destroy_category(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except response.Http404:
            return JsonResponse({'message':'No se encuentra la categoria', 'status':404}, status=404)
        except Exception as e:
            print(e)
            dicc = format_data(code=500)
            return JsonResponse(dicc, status=dicc['status'])
        return JsonResponse({'message': 'El campo fue borrado correctamente', 'status':200}, status=200)

class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # GET one User
    def get_all_users(self, request, *args, **kwargs):
        if request.user.is_authenticated ==  False:
            return JsonResponse({'success':False,'message':'No esta autenticado'}, status=401)
        validator = validate_group(request.user, ['administrator','sellers', 'checkers','buyers'])
        if validator == False and request.user.is_superuser == False:
            return JsonResponse({'success':False,'message':'No esta autorizado'}, status=403)
        val = validate_group(request.user, ['sellers','buyers', 'checkers'])
        if val == True:
            instances = User.objects.filter(id=request.user.id)
        else:
            instances = User.objects.all()
        serializer  = UserSerializer(instances, many=True)
        dicc = format_data(serializer.data, 'categorias')
        return JsonResponse(dicc, status=200)
        
    #POST new User
    def post_user(self, request, *args, **kwargs):
        try:
            serializer = UserCreatorSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            serializerRep = UserSerializer(user)   
            return JsonResponse(serializerRep.data, status=200)
        except exceptions.ValidationError as e:
            return JsonResponse({'message': e.detail, 'status':400}, status=400)
        except (exceptions.UnsupportedMediaType, exceptions.ParseError) as e:
            return JsonResponse({'message':'El formato de su request no es valido', 'status':400}, status=400)
        except Exception as e:
            print(e)
            print(type(e))
            return JsonResponse({'message':'Hubo un error en el servidor', 'status':500}, status=500)

    # GET one User
    def get_user(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            result = format_data(serializer.data)
            return JsonResponse(result, status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'message':'Hubo un error en el servidor'}, status=500) 


    # DELETE one User
    def delete_user(self, request, *args, **kwargs):
        try: 
            instance=self.get_object()
            self.perform_destroy(instance=instance)
            return JsonResponse({'message':'El usuario ha sido eliminado correctamente', 'status':200}, status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'message':'error en el server', 'status':500}, status=500)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        dataAuth = request.headers.get('Authorization')
        token = dataAuth.split(' ')[1]
        token1 = Token.objects.filter(key=token).first()
        print(type(token1))
        token1.delete()
        return JsonResponse({'message':'Token Borrado Exitosamente'}, status=200)
    
class AuthenticationView(ObtainAuthToken):
    serializer_class = AuthenticationSerializer

class TransactsView(viewsets.ModelViewSet):
    queryset = Transacts.objects.all()
    serializer_class = TransactsSerializer
    permission_classes = [IsAuthenticated, IsGroupAccepted]

    def get_all_transacts(self, request):
        sellerComp = True if IsSeller.has_permission(self, request, self.__class__) else False
        buyerComp = True if IsBuyer.has_permission(self, request, self.__class__) else False
        if sellerComp == True or buyerComp == True:
            transacts = Transacts.objects.filter(buyers_id=request.user.id)
        else:
            transacts = Transacts.objects.all()
        serializer= TransactsSerializer(transacts, many=True)   
        dicc = serializer.data
        return JsonResponse(dicc, status=200, safe=False)

    def post_transact(self, request):
        serializer = TransactsSerializer(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data, status=201)

    def delete_transact(self, request, *args, **kwargs):
        transact = self.get_object()
        buyerComp = True if IsBuyer.has_object_permission(self, request, self.__class__, transact) else False
        if buyerComp == True:
            self.perform_destroy(transact)
            return JsonResponse({'message':'Transaccion eliminada exitosamente'},status=204)
        else:
            return JsonResponse({'message':'No tiene acceso a esta'},status=404)

class GroupsView(viewsets.ModelViewSet):

    queryset = Group.objects.all()
    serializer_class = GroupsSerializer

    def nested_list(self, request):
        groups = Group.objects.all()
        serializer = GroupsSerializer(groups, many=True)
        print(serializer.data)
        return JsonResponse(serializer.data, status=200, safe=False)

class InvitationCodeView(viewsets.ModelViewSet):
    queryset = InvitationCodes.objects.all()
    serializer_class = InvitationCodesSerializer
    permission_classes = [IsAuthenticated,IsAdmin]

    def get_invitation_codes(self, request):
        invCodes = InvitationCodes.objects.all()
        result = InvitationCodesSerializer(invCodes, many=True).data
        print(result)
        return JsonResponse(result, status = 200, safe=False)

    def post_invitation_code(self, request):
        invitation = InvitationCodesSerializer(data=request.data)
        if invitation.is_valid(raise_exception=True):
            values = invitation.save()
            result = InvitationCodesSerializer(values).data
            return JsonResponse(result, status=201)
        return JsonResponse({"success":False},status=400)

