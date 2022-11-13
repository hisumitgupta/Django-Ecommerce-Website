from curses import color_content
from distutils.command.upload import upload
from email.policy import default
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User
from common.models import commonModel
from django.db.models.signals import post_save
from django.dispatch import receiver 
import uuid
from common.emails import send_account_activation_email
# from products.models import ColorVariant, Products, SizeVariant
from products.models import *
# Create your models here.





class profile(commonModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    check_email_varified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100,null=True,blank=True)
    # user_img = models.ImageField(upload_to = 'profile')

    def get_cart_count(self):
        return CartItems.objects.filter(cart__is_paid= False, cart__user=self.user).count()







class Cart(commonModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'carts')
    coupon = models.ForeignKey(Coupon,on_delete=models.SET_NULL, null=True, blank = True)
    is_paid = models.BooleanField(default=False)
    razor_pay_order_id = models.CharField(max_length = 100, null = True, blank =True)
    razor_pay_payment_id = models.CharField(max_length = 100, null = True, blank =True)
    razor_pay_payment_signature = models.CharField(max_length = 100, null = True, blank =True)

    def get_cart_total(self):
        cart_items = self.cart_items.all()
        price = [] 
        for cart_item in cart_items:
            price.append(cart_item.product.product_price)
            if cart_item.color_variant:
                color_variant_price = cart_item.color_variant.color_price
                price.append(color_variant_price)
            if cart_item.size_variant:
                size_variant_price = cart_item.size_variant.size_price  
                price.append(size_variant_price)

        if self.coupon:
            # if self.coupon.minimum_amount < sum(price):
            return sum(price) - self.coupon.discount_price   

        # print(price)
        return sum(price)










class CartItems(commonModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product  = models.ForeignKey(Products,on_delete = models.SET_NULL, null=True, blank=True)
    color_variant = models.ForeignKey(ColorVariant,on_delete=models.SET_NULL, null=True, blank=True)
    size_variant = models.ForeignKey(SizeVariant,on_delete=models.SET_NULL, null=True, blank=True)

    def get_product_price(self):
        price = [self.product.product_price]

        # if self.color_variant:
        #     color_variant_price = self.color_variant.color_price
        #     price.append(color_variant_price)
        # if self.size_variant:
        #     size_variant_price = self.size_variant.size_price
        #     price.append(size_variant_price)
        return sum(price)


 






# creating signals for as soon as login then at same time we can send email to user using signals
@receiver(post_save, sender=User)
def send_email_token(sender, instance, created, **kwargs):
    try:
        if created:
            email_token = str(uuid.uuid4())
            profile.objects.create(user= instance, email_token=email_token)
            email = instance.email
            send_account_activation_email(email, email_token)

    except Exception as e:
        print(e)



















