from django.urls import path
from .views import ProductView, CategoryView

urlpatterns = [
    path('ecommerce/',ProductView.as_view(), name='listOfProducts' ),
    path('ecommerce/categorias/', CategoryView.as_view(), name='list_of_categories'),
]