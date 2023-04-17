from django.contrib import admin
from .models import Product, Category,Transacts, User
 
# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Transacts)
admin.site.register(User)