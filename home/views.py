from itertools import product
from django.shortcuts import get_object_or_404, redirect, render
from products.models import Products
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.

def index(request):


    context = {'products': Products.objects.all()}
    return render(request, 'home/index.html', context)


def start(request):
    return render(request, "home/start.html")




def user_profile(request):
    user_data = User.objects.all().values()
    return render(request, "home/profile.html",context={'user_data':user_data})


def edit_profile(request,id):
    user = User.objects.get(id=id)
    if request.method == "POST":
        first = request.POST.get('first_name')
        last = request.POST.get('last_name')
        email = request.POST.get('email')
        user.first_name = first
        user.last_name  = last
        user.email = email
        user.save()
        # messages.success(request, 'Profile Updated')
        return redirect('product_home')
    return render(request, "home/edit_profile.html",context={'user':user})




def search_product(request):

    if request.method == 'POST':
        data = request.POST.get('search')
        try:
            product_data = Products.objects.filter(product_name__icontains=data)
            # print(product_data)
            
            return render(request, 'home/search_product.html',context={'search_data':product_data})
            
        except Exception as e:
            
            print(e)
    else:
        messages.warning(request, 'Enter Your Search')
        return render(request, 'home/search_product.html')





