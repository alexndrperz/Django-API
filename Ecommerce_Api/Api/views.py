from django.views import View
from rest_framework import viewsets
from rest_framework.response import Response
from django.http.response import JsonResponse, HttpResponse
from .models import Product,Category,Sellers,Transacts,Buyers
from .serializers import BuyerSerializer, TransactsSerializer, SellerSerializer, CategorySerializer, ProductSerializer

# from .serializers import ProductSerializer
# from rest_framework.response import Response
# from rest_framework.views imporcd apt APIView
# Create your views here.

class ProductView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    

    def finalize_response(self, request, response, *args, **kwargs):
        if response.status_code == 200:
            response.data = {
                'success' :True,
                'products' : response.data 
            }
        return super().finalize_response(request, response, *args, **kwargs)


    # def get(self, request):
    #     products = list(Product.objects.values('id', 'nameProduct','priceProduct','dateReleased', 'category_id_id'))
        
    #     for product in products:
    #         category = Category.objects.get(id=product['category_id_id'])
    #         product['category'] = category.nameCategory
    #         del product['category_id_id']

        
    #     if(len(products) > 0):
    #         data= {
    #             'message':'Success',
    #             'products':  products
    #         }
    #     else: 
    #         data={
    #             'message': 'There are no products in the database'
    #         }
    #         return HttpResponse(status=404)
    #     return JsonResponse(data)

        

    # def post(self, request):
    #     pass
    # def put(self, request):
    #     pass
    # def delete(self, request):
    #     pass


class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def finalize_response(self, request, response, *args, **kwargs):
        if response.status_code == 200:
            response.data = {
                'success' :True,
                'categories' : response.data 
            }
        return super().finalize_response(request, response, *args, **kwargs)



    #  def get(self, request, format=None):
        
    #     categories = list(Category.objects.values())
    #     products = list(Product.objects.values())
        
    #     for categorie in categories:
    #         categorieObj = Category.objects.get(id=categorie['id'])
    #         quantity = categorieObj.products_quantity
    #         categorie['products_Count'] = quantity
    #         products = Product.objects.filter(category_id=categorie['id'])
    #         categorie['products'] = list(products.values('id','nameProduct','active'))


    #     if(len(categories) > 0):
    #         data = {
    #             'message': 'Success',
    #             'categories':categories,
    #         }
    #     else:
    #         data = {
    #             'message':'Fail'
    #         }
        
            
    #     return JsonResponse(data)


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

    # def get(self, request, format=None):
    #     sellers = list(Sellers.objects.values())
    #     products = list(Product.objects.values('id', 'nameProduct','priceProduct','dateReleased', 'category_id_id','seller_id_id'))
        

    #     for product in products:
    #         category = Category.objects.get(id=product['category_id_id'])
    #         product['category'] = category.nameCategory
    #         del product['category_id_id']

    #     for seller in sellers:
    #         productsSeller = Product.objects.filter(seller_id_id = seller['id'])
    #         products_list = []
    #         for product in productsSeller:
    #             products = {
    #                 'id': product.nameProduct,
    #                 'nameProduct': product.priceProduct,
    #                 'dateReleased': product.dateReleased,
    #                 'active': product.active
    #             }
    #             products_list.append(products)
    #         seller['products'] = products_list
    #     if(len(sellers) > 0):
    #         data = {
    #             'message': 'Success',   
    #             'sellers': sellers
    #         }
    #     else:
    #         data = {
    #             'message': 'Faill'
    #         }
    #     return JsonResponse(data)

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

    # def get(self, request, format=None):
    #     transacts = list(Transacts.objects.values())
    #     products = list(Product.objects.values())
    #     buyers = list(Buyers.objects.values())
    #     sellers = list(Sellers.objects.values())

    #     # Serializers, estas lineas estan proximas a cambiarse
    #     for buyer in buyers:
    #         buyer['dateRegister'] = buyer['dateRegister'].strftime('%m/%d/%Y %I:%M:%S %p')

    #     for product in products:
    #         category = Category.objects.get(id=product['category_id_id'])
    #         product['category'] = category.nameCategory
    #         seller = list(filter(lambda x:x['id']==product['seller_id_id'],sellers))
    #         product['seller'] = seller[0]
    #         del product['category_id_id']
    #         del product['seller_id_id']
    #         del product['active']

            
    #     for transact in transacts:
    #         transact['dateTransact'] = transact['dateTransact'].strftime('%m/%d/%Y %I:%M:%S %p')
    #         product = list(filter(lambda x:x['id']==transact['product_id'],products))
    #         buyer = list(filter(lambda x:x['id']==transact['buyers_id'],buyers))
    #         transact['product'] = product[0] 
    #         transact['buyer'] = buyer[0]
    #         del transact['product_id']
    #         del transact['buyers_id']
    #     #---------------
    #     if(len(transacts) > 0):
    #         data = {
    #             'message': 'Success',
    #             'transacts': transacts
    #         }
    #     return JsonResponse(data)
    


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
 
    # def get(self, request, format=None):
    #     buyers = list(Buyers.objects.values())

    #     if(len(buyers) > 0):
    #         data = {
    #             'message': 'Success',   
    #             'buyers': buyers
    #         }
    #     else:
    #         data = {
    #             'message': 'Fail'
    #         }
    #     return JsonResponse(data) 