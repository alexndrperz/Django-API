from django.views import View
from django.http.response import JsonResponse, HttpResponse
from .models import Product,Category
from .serializers import ProductSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
# Create your views here.

class ProductView(View):
    
    def get(self, request):

        products = list(Product.objects.values())
        if(len(products) > 0):
            data= {
                'message':'Success',
                'products':products
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


class CategoryView(APIView):
     def get(self, request, format=None):

        categories = Category.objects.all()
        products = Product.objects.all()

        # Creamos un diccionario donde almacenaremos las categorias y sus productos
        data = {}
        for category in categories:
            serializer = ProductSerializer(products.filter(category_id=category.id), many=True)
            data[category.nameCategory] = {'products':serializer.data}

        return JsonResponse(data)