from django.contrib import admin
from .models import Product, Category, Sellers
 
# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Sellers)