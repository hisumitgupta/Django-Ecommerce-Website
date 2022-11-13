from email.policy import default
from pyexpat import model
from django.db import models
from common.models import commonModel
from django.utils.text import slugify

# Create your models here.



class Category(commonModel):
    category_name = models.CharField(max_length=150)
    category_slug =  models.SlugField(unique=True, null=True, blank=True)
    category_img = models.ImageField(upload_to='categories')



    def save(self, *args, **kwargs):
        self.category_slug = slugify(self.category_name)
        super(Category, self).save(*args, **kwargs)



    def __str__(self):
        return self.category_name


class ColorVariant(commonModel):
    color_name = models.CharField(max_length=100)
    color_price = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.color_name




class SizeVariant(commonModel):
    size_name = models.CharField(max_length=100)
    size_price = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.size_name




class Products(commonModel):
    product_name = models.CharField(max_length=50,)
    product_slug =  models.SlugField(unique=True,null=True,blank=True)
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    product_price = models.IntegerField()
    product_desc = models.TextField()
    color_variant = models.ManyToManyField(ColorVariant , blank=True)
    size_variant = models.ManyToManyField(SizeVariant , blank=True)
    

    
    def save(self, *args, **kwargs):
        self.product_slug = slugify(self.product_name)
        super(Products, self).save(*args, **kwargs)



    def __str__(self):
        return self.product_name


    def get_product_price_by_size(self,size):
        return self.product_price + SizeVariant.objects.get(size_name = size).size








class Product_img(commonModel):
    products = models.ForeignKey(Products,on_delete=models.CASCADE, related_name='products_images')
    img = models.ImageField(upload_to='products')





class Coupon(commonModel):
    coupon_code = models.CharField(max_length=10)
    is_expired = models.BooleanField(default=False)
    discount_price = models.IntegerField(default=100)
    minimum_amount = models.IntegerField(default=500)
























