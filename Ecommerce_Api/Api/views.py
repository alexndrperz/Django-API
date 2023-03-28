from django.views import View
from django.http.response import JsonResponse, HttpResponse
from .models import Product
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