from django.urls import path
from .views import ProductView, CategoryView,SellersView,TransactsView,BuyersView,UserView
from django.views.decorators.csrf import ensure_csrf_cookie

urlpatterns = [
    path('productos/',ProductView.as_view({'get':'list'}), name='listOfProducts' ),
    path('categorias', CategoryView.as_view({'get':'nested_list_categories', 'post':'post_category'}), name='list_of_categories'),
    path('categorias/<int:pk>', CategoryView.as_view({'put': 'update_category', 'get':'get_category','delete':'destroy_category'}, name='Update_and_Get_Categorie')),
    path('users',UserView.as_view({'get':'list'}), name='List_Users'),
    path('vendedores/',SellersView.as_view({'get':'list'}), name='listOfSellers'),
    path('transacts/',TransactsView.as_view({'get':'list'}), name='listOfTransacts'),
    path('buyers/',BuyersView.as_view({'get': 'list'}), name='listOfBuyers')
]