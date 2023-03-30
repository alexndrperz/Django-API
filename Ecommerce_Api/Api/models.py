from django.db import models

# Create your models here.
class Sellers(models.Model):
    nameSeller = models.CharField(max_length=50)
    lastNameSeller = models.CharField(max_length=50)
    registerDate =  models.DateField(auto_now_add=True)

class Category(models.Model):
    nameCategory = models.CharField(max_length=50)
    @property
    def products_quantity(self):
        return self.product_set.count()

class Product(models.Model):
    nameProduct = models.CharField(max_length=50)
    priceProduct = models.CharField(max_length=50)
    dateReleased = models.DateField(auto_now_add=True)
    active = models.BooleanField(default="false")
    seller_id = models.ForeignKey(Sellers, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)


