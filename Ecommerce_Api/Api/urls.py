from django.urls import path
from .views import ProductView, CategoryView,SellersView,TransactsView,BuyersView

urlpatterns = [
    path('productos/',ProductView.as_view(), name='listOfProducts' ),
    path('categorias/', CategoryView.as_view(), name='list_of_categories'),
    path('vendedores/',SellersView.as_view(), name='listOfSellers'),
    path('transacts/',TransactsView.as_view(), name='listOfTransacts'),
    path('buyers/',BuyersView.as_view(), name='listOfBuyers')

]