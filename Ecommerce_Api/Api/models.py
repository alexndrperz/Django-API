from django.db import models   
from datetime import datetime
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
    Group
)

from django.utils.timezone import now, timedelta 

print(now())

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
    is_digital = models.BooleanField(default=False)
    seller_id = models.ForeignKey(User, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)

class Transacts(models.Model):
    dateTransact = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,  default=1)
    buyers = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

class InvitationCodes(models.Model):
    invitationCodes = models.CharField(max_length=8)
    description = models.CharField(max_length=50)
    is_used = models.BooleanField(default=False)
    is_expired = models.BooleanField(default=False)
    realeased_date = models.DateTimeField(auto_now_add=True)
    expire_date = models.DateTimeField(default=now() + timedelta(days=7))
    
    def save(self, *args, **kwargs):
        if self.expire_date < timezone.now():
            self.is_expired = True
        super().save(*args, **kwargs)


