from django.db import models   
from datetime import datetime
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
    Group
)

class UserManager(BaseUserManager):
    def create_user(self,email, password, **args):
        if not email:
            raise ValueError('Falta email')
        user = self.model(email=email, **args)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, password, **args):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user 

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    name  = models.CharField(max_length=50)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    registro = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'

    objects = UserManager()

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
    active = models.BooleanField(default=False)
    seller_id = models.ForeignKey(Sellers, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)

class Buyers(models.Model):
    nameBuyer = models.CharField(max_length=50)
    lastNameBuyer = models.CharField(max_length=50)
    dateRegister = models.DateTimeField(auto_now_add=True)

class Transacts(models.Model):
    dateTransact = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,  default=1)
    buyers = models.ForeignKey(Buyers, on_delete=models.CASCADE, default=1)


