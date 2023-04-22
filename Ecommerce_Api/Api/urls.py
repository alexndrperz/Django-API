from django.urls import path
from .views import ProductView, CategoryView,TransactsView,UserView, AuthenticationView, GroupsView

urlpatterns = [
    path('productos',ProductView.as_view({'get':'nested_list_products','post':'post_product'}), name='listOfProducts' ),
    path('productos/<int:pk>',ProductView.as_view({'get':'get_product', 'delete':'delete_product','put':'update_product'}), name='listOfProducts' ),
    path('d-products',ProductView.as_view({'get':'get_digital_products'})),
    path('categorias', CategoryView.as_view({'get':'nested_list_categories', 'post':'post_category'}), name='list_of_categories'),
    path('categorias/<int:pk>', CategoryView.as_view({'put': 'update_category', 'get':'get_category','delete':'destroy_category'}, name='Update_and_Get_Categorie')),
    path('groups', GroupsView.as_view({'get':'nested_list'}), name='Groups_list'),
    path('users',UserView.as_view({'get':'get_all_users','post':'post_user'}), name='List_Users'),
    path('users/authenticate',AuthenticationView.as_view(), name='Get_token'),
    path('users/<int:pk>', UserView.as_view({'get':'get_user','delete':'delete_user'})),
    path('transacts/',TransactsView.as_view({'get':'get_all_transacts'}), name='listOfTransacts'),
]