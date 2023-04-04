from django.views import View
from django.http.response import JsonResponse, HttpResponse
from .models import Product,Category,Sellers
# from .serializers import ProductSerializer
# from rest_framework.response import Response
# from rest_framework.views imporcd apt APIView
# Create your views here.

class ProductView(View):
    
    def get(self, request):
        products = list(Product.objects.values('id', 'nameProduct','priceProduct','dateReleased', 'category_id_id'))
        
        for product in products:
            category = Category.objects.get(id=product['category_id_id'])
            product['category'] = category.nameCategory
            del product['category_id_id']

        
        if(len(products) > 0):
            data= {
                'message':'Success',
                'products':  products
            }
        else: 
            data={
                'message': 'There are no products in the database'
            }
            return HttpResponse(status=404)
        return JsonResponse(data)

        

    def post(self, request):
        pass
    def put(self, request):
        pass
    def delete(self, request):
        pass


class CategoryView(View):
     def get(self, request, format=None):
        
        categories = list(Category.objects.values())
        products = list(Product.objects.values())
        
        for categorie in categories:
            categorieObj = Category.objects.get(id=categorie['id'])
            quantity = categorieObj.products_quantity
            categorie['products_Count'] = quantity
            products = Product.objects.filter(category_id=categorie['id'])
            categorie['products'] = list(products.values('id','nameProduct','active'))


        if(len(categories) > 0):
            data = {
                'message': 'Success',
                'categories':categories,
            }
        else:
            data = {
                'message':'Fail'
            }
        
            
        return JsonResponse(data)


class SellersView(View):
    def get(self, request, format=None):
        sellers = list(Sellers.objects.values())
        data = {
            'message': 'Success',   
            'sellers': sellers
        }
        return JsonResponse(data)