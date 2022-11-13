from django.contrib import admin
from products.models import *
# Register your models here.

admin.site.register(Category)

admin.site.register(Coupon)

class ProductImageAdmin(admin.StackedInline): # here we getting the model which we have to add in product model
    model = Product_img

class ProductAdmin(admin.ModelAdmin): #here we modifying the admin page with ModelAdmin or merging
    list_display = ['product_name', 'product_price']
    inlines= [ProductImageAdmin]



@admin.register(ColorVariant)
class ColorVariantAdmin(admin.ModelAdmin):
    list_display = ['color_name','color_price']
    model = ColorVariant




@admin.register(SizeVariant)
class SizeVariantAdmin(admin.ModelAdmin):
    list_display = ['size_name','size_price']
    model = SizeVariant


admin.site.register(Products,ProductAdmin) # here we are passing merge model in Product model
admin.site.register(Product_img)











