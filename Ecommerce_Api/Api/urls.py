from django.urls import path
from .views import ProductView, CategoryView,SellersView,TransactsView,BuyersView
from django.views.decorators.csrf import ensure_csrf_cookie

urlpatterns = [
    path('productos/',ProductView.as_view({'get':'list'}), name='listOfProducts' ),
    path('categorias', CategoryView.as_view({'get':'nested_list_categories', 'post':'post_category'}), name='list_of_categories'),
    path('vendedores/',SellersView.as_view({'get':'list'}), name='listOfSellers'),
    path('transacts/',TransactsView.as_view({'get':'list'}), name='listOfTransacts'),
    path('buyers/',BuyersView.as_view({'get': 'list'}), name='listOfBuyers')
]