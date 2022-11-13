from contextlib import redirect_stderr
import re
from wsgiref.util import request_uri
from django.shortcuts import render

from products.models import Products, SizeVariant



# Create your views here.

def product_data(request, slug):

    try:


        product = Products.objects.get(product_slug = slug)
        context = {'product':product}
        if request.GET.get('size'):
            size = request.GET.get('size')
            price = product.get_product_price_by_size(size)
            context['selected_size'] = size
            context['updated_price'] = price
            print(price)

        return render(request, 'products/product.html', context=context)
    except Exception as e:
        print(e)
    
    # return render(request, 'products/product.html')