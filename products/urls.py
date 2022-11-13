
from django.urls import path,include
from products.views import *

urlpatterns = [
    path('<slug>/',product_data,name='product_data'),
    
]

