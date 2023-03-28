from django.urls import path
from .views import ProductView

urlpatterns = [
    path('ecommerce/',ProductView.as_view(), name='listOfProducts' )
]