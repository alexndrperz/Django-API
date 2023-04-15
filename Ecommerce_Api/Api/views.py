from django.views import View
from django.http import response
from rest_framework import viewsets,permissions, authentication,mixins, exceptions
from rest_framework.permissions import IsAuthenticated
from django.http.response import JsonResponse 
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import  ObtainAuthToken
from django.contrib.auth.models import Group
from .models import Product,Category,Sellers,Transacts,Buyers,User
from .serializers import (BuyerSerializer, 
                          TransactsSerializer, 
                          SellerSerializer, 
                          CategorySerializer,
                          CategoryWithoutProductsSerializer, 
                          ProductSerializer,
                          ProductCreatorSerializer,
                          UserSerializer,
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

    # GET all Products (with restrictions for sellers)
    def nested_list_products(self, request):
        if request.user.is_authenticated ==  False:
            return JsonResponse({'success':False,'message':'No esta autenticado'}, status=401)
        validator = validate_group(request.user, ['administrator','sellers', 'checkers'])
        if validator == False and request.user.is_superuser == False:
            return JsonResponse({'success':False,'message':'No esta autorizado'}, status=403)
        if validate_group(request.user, ['sellers']):
            products = Product.objects.filter(seller_id=request.user.id)
            serializer= ProductSerializer(products, many=True)   
            data = serializer.data
        return JsonResponse(list(data), status=200,safe=False)
    # GET just one product (Also with restricctions)
    def get_product(self, request, *args, **kwargs):
        try:
            
            if request.user.is_authenticated ==  False:
                return JsonResponse({'success':False,'message':'No esta autenticado'}, status=401)
            validator = validate_group(request.user, ['administrator','sellers', 'checkers'])
            instance = self.get_object()
            if validator == False and request.user.is_superuser == False:
                return JsonResponse({'success':False,'message':'No esta autorizado'}, status=403)
            if validate_group(request.user, ['sellers']):
                if instance.seller_id.id != request.user.id:
                    return JsonResponse({'success':False, 'message':'No ha vendido este producto'}, status=404)
            serializer = self.get_serializer(instance)
            return JsonResponse(serializer.data,status=200)
        except Exception as e:
            print(e)
            print(type(e))
            return JsonResponse({}, status=500)
    # POST a new product (Taking Seller id)
    def post_product(self,request):
        if request.user.is_authenticated ==  False:
            return JsonResponse({'success':False,'message':'No esta autenticado'}, status=401)
        validator = validate_group(request.user, ['administrator','sellers', 'checkers'])
        if validator == False and request.user.is_superuser == False:
            return JsonResponse({'success':False,'message':'No esta autorizado'}, status=403)
        serializer = ProductCreatorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        self.get_success_headers(serializer.data)
        dicc = serializer.data
        groupUser = Group.objects.get(id=request.user.groups.values_list('id', flat=True)[0])
        dicc['seller_id'] = {
            'id':request.user.id,
            'name':request.user.name,
            'email':request.user.email,
            'group':str(groupUser)
        } 

        return JsonResponse(dicc, status=200)
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
        serializer.save(seller_id=self.request.user)
        print("asasd")




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
            dicc['user'] = {
                'id': request.user.id,
                'name': request.user.name,
                'email': request.user.email,
                'group': list(request.user.groups.values_list('name', flat=True))
            }
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
        try:
            instances = User.objects.all()
            serializer  = UserSerializer(instances, many=True)
            dicc = format_data(serializer.data, 'categorias')
            return JsonResponse(dicc, status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'message':'Hubo un error en el servidor'}, status=500)
    
    #POST new User
    def post_user(self, request, *args, **kwargs):
        try:
            group_name= request.data.pop('groups', None)
            print(group_name)
 
            group= Group.objects.get(name=group_name)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            user.groups.add(group)
            finaldicc = serializer.data
            finaldicc['groups'] = group_name
            
            header = self.get_success_headers(serializer.data)
            return JsonResponse(finaldicc, status=200, headers=header)
        except exceptions.ValidationError as e:
            return JsonResponse({'message': e.detail, 'status':400}, status=400)
        except (exceptions.UnsupportedMediaType, exceptions.ParseError) as e:
            return JsonResponse({'message':'El formato de su request no es valido', 'status':400}, status=400)
        # except Exception as e:
        #     print(e)
        #     print(type(e))
        #     return JsonResponse({'message':'Hubo un error en el servidor', 'status':500}, status=500)

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
    
class AuthenticationView(ObtainAuthToken):
    serializer_class = AuthenticationSerializer

class SellersView(viewsets.ModelViewSet):
    queryset = Sellers.objects.all()
    serializer_class = SellerSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        if response.status_code == 200:
            response.data = {
                'success' :True,
                'sellers' : response.data 
            }
        return super().finalize_response(request, response, *args, **kwargs)

class TransactsView(viewsets.ModelViewSet):
    queryset = Transacts.objects.all()
    serializer_class = TransactsSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        if response.status_code == 200:
            response.data = {
                'success' :True,
                'transacts' : response.data 
            }
        
        return super().finalize_response(request, response)
    
class BuyersView(viewsets.ModelViewSet):
    queryset = Buyers.objects.all()
    serializer_class = BuyerSerializer

    def finalize_response(self,request, response, *args,**kwargs):
        
        if response.status_code == 200:
            response.data   = {
                'success': True,
                'buyers': response.data
            }
        return super().finalize_response(request, response)

class GroupsView(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupsSerializer

    def nested_list(self, request):
        groups = list(Group.objects.all())
        data = [{'id':group.id, 'name':group.name}for group in groups]
        data = format_data(data, nameClass='groups')
        return JsonResponse(data, status=200)