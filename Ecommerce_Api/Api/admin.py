from django.contrib import admin
from .models import Product, Category, Sellers,Transacts,Buyers, User
 
# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Sellers)
admin.site.register(Buyers)
admin.site.register(Transacts)
admin.site.register(User)