from django.urls import path
from .views import ProductView, CategoryView,SellersView

urlpatterns = [
    path('ecommerce/productos/',ProductView.as_view(), name='listOfProducts' ),
    path('ecommerce/categorias/', CategoryView.as_view(), name='list_of_categories'),
    path('ecommerce/vendedores/',SellersView.as_view(), name='listOfSellers')
]