import re
from django.http import HttpResponseRedirect
from django.shortcuts import HttpResponse, render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import profile,Cart,CartItems
from products.models import Products, SizeVariant,Coupon
from django.http import HttpResponseRedirect,HttpResponse
import razorpay




# Create your views here.


def login_page(request):

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        Check_user = User.objects.filter(username = email)
        print(Check_user)


        if not Check_user.exists() :
            messages.warning(request, 'Account Not Found')
            return HttpResponseRedirect(request.path_info)

        if not Check_user[0].profile.check_email_varified:
            messages.warning(request, 'Your Account is not Varified')
            return HttpResponseRedirect(request.path_info)

        login_user = authenticate( username = email, password = password)
        if login_user:
            login(request, login_user)
            return redirect('home')
        
        messages.warning(request, 'Invalid Email and Password')
        return HttpResponseRedirect(request.path_info)


    return render(request,'accounts/login.html')






def register_page(request):
    if request.method == "POST":
        firstName = request.POST.get('first_name')
        lastName = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        Check_user = User.objects.filter(username = email)
        if Check_user.exists():
            messages.warning(request, 'Email already Exits')
            return HttpResponseRedirect(request.path_info)

        else:
            Create_user = User.objects.create(first_name=firstName ,last_name = lastName, email=email ,username=email)
            Create_user.set_password(password)
            Create_user.save()
            messages.success(request, 'An Email has been Sent to Your Mail')
            return HttpResponseRedirect(request.path_info)
            

    return render(request, 'accounts/register.html')



def logout_view(request):
    logout(request)
    return redirect('login_page')
    return redirect(request, 'accounts/logout.html')




def email_activation(request, email_token):
    try:
        user = profile.objects.get(email_token = email_token)
        user.check_email_varified = True
        user.save()
        return redirect('login_page')
    except Exception as e:
        return HttpResponse('Invalid Email')




def add_to_cart(request, uid):
    variant = request.GET.get('variant')
    product = Products.objects.get(uid = uid)
    user = request.user
    cart , _ = Cart.objects.get_or_create(user = user, is_paid=False)

    cart_item = CartItems.objects.create(cart=cart, product=product)


    if variant:
        variant = request.GET.get('variant')
        size_variant = SizeVariant.objects.get(size_name= variant)
        cart_item.size_variant = size_variant
        cart_item.save()

    if cart_item == "":
        print('******************nocart*************************')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))




def remove_cart(request, cart_item_uid):
    try:
        cart_item = CartItems.objects.get(uid = cart_item_uid)
        cart_item.delete()
    except Exception as e:
        print(e)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))







from django.conf import settings
def cart(request):
    cart_obj = None
    try:
        cart_obj = Cart.objects.get(is_paid= False, user=request.user)
        
    except Exception as e:
        print(e)    
    if request.method == "POST":
        coupon = request.POST.get('coupon')
        coupon_obj = Coupon.objects.filter(coupon_code__icontains = coupon)
        if not coupon_obj.exists():
            messages.warning(request, 'Invalid Coupan')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        if cart_obj.coupon:
            messages.warning(request, 'Coupon alredy Exits')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if cart_obj.get_cart_total() < coupon_obj[0].minimum_amount:
            messages.warning(request, f'Amount should be greathan {coupon.obj[0].minimum_amount}')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if coupon_obj[0].is_expired:
            messages.warning(request, f'Coupon Expired')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


        cart_obj.coupon = coupon_obj[0]
        cart_obj.save()
        messages.success(request, 'Coupon applied')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
  
    if cart_obj: 
        try:

            client = razorpay.Client(auth = (settings.KEY, settings.SECRET))
            payment = client.order.create({'amount': cart_obj.get_cart_total()*100, 'currency': "INR", 'payment_capture': '1'})
            cart_obj.razor_pay_order_id = payment['id']
            cart_obj.save()
            # print(payment)
        except Exception as e:
            print(e)
            return render(request, 'accounts/cart.html')

    else:
        payment = None


  

    context = {'cart': cart_obj, 'payment': payment}
    return render(request, 'accounts/cart.html',context)

    

def remove_coupon(request, cart_id):
    cart = Cart.objects.get(uid=cart_id)
    cart.coupon = None
    cart.save()
    messages.success(request, 'Coupon Removed')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



def success(request):
    order_id = request.GET.get('order_id')
    cart = Cart.objects.get(razor_pay_order_id=order_id)
    cart.is_paid = True
    cart.save()
    return HttpResponse('Payment Success')






