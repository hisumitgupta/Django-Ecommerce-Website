
from django.urls import path,include
from home.views import *

urlpatterns = [
    path('',start,name='home'),
    path('product-home/',index,name='product_home'),
    
    path('user-profile/',user_profile,name='user_profile'),
    path('edit-profile/<id>',edit_profile,name='edit_profile'),
    path('search-product/',search_product,name='search_product'),
 

]

