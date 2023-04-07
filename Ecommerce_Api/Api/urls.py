from django.urls import path
from .views import ProductView, CategoryView,SellersView,TransactsView,BuyersView

urlpatterns = [
    path('productos/',ProductView.as_view({'get':'list'}), name='listOfProducts' ),
    path('categorias/', CategoryView.as_view({'get':'list'}), name='list_of_categories'),
    path('vendedores/',SellersView.as_view({'get':'list'}), name='listOfSellers'),
    path('transacts/',TransactsView.as_view({'get':'list'}), name='listOfTransacts'),
    path('buyers/',BuyersView.as_view({'get': 'list'}), name='listOfBuyers')

]