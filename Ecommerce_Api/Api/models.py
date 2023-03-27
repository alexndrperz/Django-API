from django.db import models

# Create your models here.
class Product(models.Model):
    # idProduct = models.AutoField()
    nameProduct = models.CharField(max_length=50)
    priceProduct = models.CharField(max_length=30)
    dateReleased = models.DateField()