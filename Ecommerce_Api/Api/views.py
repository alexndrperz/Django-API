from django.views import View
from rest_framework import viewsets,permissions, authentication,mixins
from rest_framework.permissions import IsAuthenticated
from django.http.response import JsonResponse 
from .models import Product,Category,Sellers,Transacts,Buyers
from .serializers import BuyerSerializer, TransactsSerializer, SellerSerializer, CategorySerializer, ProductSerializer

def format_data(data, nameClass, error=False):
    status = 0
    if error:
        return {'message':'Ha habido un error en el servidor', 'status':500}
    if (len(data) > 0):
        result = {
            'success':True,
            nameClass:data,
            'status':200
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

    #GET ALL
    def nested_list_categories(self, request):
        try: 
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
            dicc = format_data(serializer.data, 'categorias')
            return JsonResponse(dicc, status=dicc['status'])   
        except:
            return JsonResponse()





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
