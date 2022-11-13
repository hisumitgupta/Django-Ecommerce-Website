from django.urls import path
from User_account.views import *


urlpatterns = [
    path('login/', login_page, name="login_page"),
    path('register/',register_page, name="register_page"),
    path('logout/',logout_view, name="logout"),
    path('activate/<email_token>/', email_activation,name='email_activation'),
    path('cart/',cart,name='cart'),
    path('add-to-cart/<uid>/',add_to_cart,name='add_to_cart'),
    path('remove-cart/<cart_item_uid>/',remove_cart,name="remove_cart"),
    path('remove-coupon/<cart_id>/',remove_coupon,name="remove_coupon"),
    path('success/',success,name="success"),

]





