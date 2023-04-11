from django.views import View
from django.http import response
from rest_framework import viewsets,permissions, authentication,mixins, exceptions
from rest_framework.permissions import IsAuthenticated
from django.http.response import JsonResponse 
from .models import Product,Category,Sellers,Transacts,Buyers,User
from .serializers import (BuyerSerializer, 
                          TransactsSerializer, 
                          SellerSerializer, 
                          CategorySerializer,
                          CategoryWithoutProductsSerializer, 
                          ProductSerializer,
                          UserSerializer)

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

class ProductView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]
    

    def finalize_response(self, request, response, *args, **kwargs):
        if response.status_code == 200:
            if len(response.data) == 0:
                return JsonResponse({'message':'Fail'}, status=404)
            response.data = {
                'success' :True,
                'products' : response.data 
            }
            
        return super().finalize_response(request, response, *args, **kwargs)





class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    #GET all Categories
    def nested_list_categories(self, request):
        try: 
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
                return JsonResponse({'message':'Ha dejado uno o mas campos requeridos vacios', 'status':400}, status=400)
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
