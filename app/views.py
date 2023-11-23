from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
from django.views import View
from django.db.models import Q
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
import json

class ProductView(View):
 def get(self, request):
  topwears = Product.objects.filter(category = 'TW')
  bottomwears = Product.objects.filter(category = 'BW')
  mobiles = Product.objects.filter(category = 'M')
  laptops = Product.objects.filter(category = 'L')

  context = {
   'topwears':topwears,
   'bottomwears':bottomwears,
   'mobiles':mobiles,
   'laptops':laptops,
  }
  return render(request, 'app/home.html', context)

# def home(request):
#  return render(request, 'app/home.html')


class ProductDetailView(View):
 def get(self, request, pk):
  product = Product.objects.get(pk= pk)
  item_already_in_cart = False

  if request.user.is_authenticated:
    item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user = request.user)).exists()
  context = {
   'product':product,
   'item_already_in_cart' : item_already_in_cart,
  }
  return render(request, 'app/productdetail.html', context)
 

# def product_detail(request, pk):
#     product = Product.objects.get(pk= pk)
#     context = {
#      'product':product,
#      }
#     return render(request, 'app/productdetail.html', context)

def add_to_cart(request):
 if request.user.is_authenticated:
  user = request.user
  product_id = request.GET.get('prod_id')
  product = Product.objects.get(pk = product_id)
  Cart(user = user, product = product).save()
  return redirect('/cart')
 return redirect('/accounts/login')

def show_cart(request):
 if request.user.is_authenticated:
  usr = request.user
  cart = Cart.objects.filter(user = usr)
  amount = 0.0
  shipping_amount = 70.0
  total_amount = 0.0

  cart_product = [p for p in Cart.objects.all() if p.user == usr]
  
  if cart_product:
   for p in cart_product:
    tempamount = (p.quantity * p.product.discounted_price)
    amount +=tempamount
  context = {
   'carts' : cart,
   'amount' : amount,
   'total_amount' : amount + shipping_amount,
  }
  return render(request, 'app/addtocart.html', context)
 return redirect('/accounts/login')

def plus_cart(request):
  data = json.loads(request.body)
  prod_id = data['productId']
  c = Cart.objects.get(Q(product = prod_id) & Q(user = request.user))
  c.quantity += 1
  c.save()
  amount = 0.0
  shipping_amount = 70.0
  total_amount = 0.0

  cart_product = [p for p in Cart.objects.all() if p.user == request.user]
  for p in cart_product:
    tempamount = (p.quantity * p.product.discounted_price)
    amount +=tempamount
  data = {  
   'quantity' : c.quantity,
   'amount' : amount,
   'total_amount' : amount + shipping_amount,
  }
  return JsonResponse(data, safe=False)

def minus_cart(request):
  data = json.loads(request.body)
  prod_id = data['productId']
  c = Cart.objects.get(Q(product = prod_id) & Q(user = request.user))
  c.quantity -= 1
  c.save()


  if c.quantity <= 0:
   c.delete()
   
  if c is None:
   quantity = 0
  else:
   quantity = c.quantity
  
  amount = 0.0
  shipping_amount = 70.0
  total_amount = 0.0

  cart_product = [p for p in Cart.objects.all() if p.user == request.user]
  for p in cart_product:
    tempamount = (p.quantity * p.product.discounted_price)
    amount +=tempamount
  data = {  
   'quantity' : quantity,
   'amount' : amount,
   'total_amount' : amount + shipping_amount,
  }
  return JsonResponse(data, safe=False)

def remove_cart(request):
  data = json.loads(request.body)
  prod_id = data['productId']
  c = Cart.objects.get(Q(product = prod_id) & Q(user = request.user))
  c.delete()
  amount = 0.0
  shipping_amount = 70.0
  total_amount = 0.0

  cart_product = [p for p in Cart.objects.all() if p.user == request.user]
  for p in cart_product:
    tempamount = (p.quantity * p.product.discounted_price)
    amount +=tempamount
  data = {
   'amount' : amount,
   'total_amount' : amount + shipping_amount,
  }
  return JsonResponse(data, safe=False)
 

def get_cart_quantity(request):
 usr = request.user
 cart = Cart.objects.filter(user = usr)
 data = len(cart)
 return JsonResponse(data, safe=False)

def buy_now(request):
 return render(request, 'app/buynow.html')

# def profile(request):
#  return render(request, 'app/profile.html')

class ProfileView(View):
 def get(self, request):
  if request.user.is_authenticated:
    form = CustomerProfileForm()
    context = {
    'form' : form,
    'active' : 'btn-primary'
    }
    return render(request, 'app/profile.html', context)
  return redirect('/accounts/login')
 
 def post(self, request):
  form = CustomerProfileForm(request.POST)
  if form.is_valid():
   usr = request.user
   name = form.cleaned_data['name']
   locality = form.cleaned_data['locality']
   city = form.cleaned_data['city']
   state = form.cleaned_data['state']
   zipcode = form.cleaned_data['zipcode']

   reg = Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode)

   reg.save()

   messages.success(request, 'Congratulations!! Profile Updated Successfully')

  return render(request, 'app/profile.html', {'form' : form, 'active': 'btn-primary'})

def address(request):
 adr = Customer.objects.filter(user = request.user)
 context = {'address' : adr, 'active' : 'btn-primary'}
 return render(request, 'app/address.html', context)

def orders(request):
 usr = request.user
 op = OrderPlaced.objects.filter(user = usr)
 context = {
  'op' : op
 }
 return render(request, 'app/orders.html', context)

# def change_password(request):
#  return render(request, 'app/changepassword.html')

def mobile(request, data = None):
 if data == 'One-Plus':
  data = 'One Plus'
 if data == None:
  mobiles = Product.objects.filter(category = 'M')
 elif data == 'Poco' or data == 'One Plus':
  mobiles = Product.objects.filter(category = 'M').filter(brand = data)
 elif data == 'below':
  mobiles = Product.objects.filter(category = 'M').filter(discounted_price__lt =  10000)
 elif data == 'above':
  mobiles = Product.objects.filter(category = 'M').filter(discounted_price__gte =  10000)
 context = {
 'mobiles':mobiles,
 }
 return render(request, 'app/mobile.html', context)

def laptop(request, data = None):
 if data == None:
  laptops = Product.objects.filter(category = 'L')
 elif data == 'below':
  laptops = Product.objects.filter(category = 'L').filter(discounted_price__lt =  50000)
 elif data == 'above':
  laptops = Product.objects.filter(category = 'L').filter(discounted_price__gte =  50000)
 else:
  laptops = Product.objects.filter(category = 'L').filter(brand =  data)
 context = {
 'laptops':laptops,
 }
 return render(request, 'app/laptop.html', context)

def topwears(request, data = None):
 if data == None:
  topwears = Product.objects.filter(category = 'TW')
 elif data == 'below':
  topwears = Product.objects.filter(category = 'TW').filter(discounted_price__lt =  500)
 elif data == 'above':
  topwears = Product.objects.filter(category = 'TW').filter(discounted_price__gte =  500)
 elif data == 'HandM':
  topwears = Product.objects.filter(category = 'TW').filter(brand = 'H&M')
 else:
  topwears = Product.objects.filter(category = 'TW').filter(brand =  data)
 context = {
 'topwears':topwears,
 }
 return render(request, 'app/topwear.html', context)

def bottomwears(request, data = None):
 if data == None:
  bottomwears = Product.objects.filter(category = 'BW')
 elif data == 'below':
  bottomwears = Product.objects.filter(category = 'BW').filter(discounted_price__lt =  300)
 elif data == 'above':
  bottomwears = Product.objects.filter(category = 'BW').filter(discounted_price__gte =  300)
 else:
  bottomwears = Product.objects.filter(category = 'BW').filter(brand =  data)
 context = {
 'bottomwears':bottomwears,
 }
 return render(request, 'app/bottomwear.html', context)




# def login(request):
#  return render(request, 'app/login.html')

# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')

class CustomerRegistrationView(View):
 def get(self, request):
  form = CustomerRegistrationForm()
  context = {'form' : form}
  return render(request, 'app/customerregistration.html', context)
 
 def post(self, request):
  form = CustomerRegistrationForm(request.POST)
  if form.is_valid():
   messages.success(request, 'Congratulations!! Registered Successfully')
   form.save()
  context = {'form' : form}
  return render(request, 'app/customerregistration.html', context)

def checkout(request, productId = None):
 if request.user.is_authenticated:
  usr = request.user
  user_address = Customer.objects.filter(user = usr)
  amount = 0.0
  shipping_amount = 70.0
  total_amount = 0.0

  direct_buy = False
  product = []

  if productId is None:
    cart_items = Cart.objects.filter(user = usr)
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
      for p in cart_product:
        tempamount = (p.quantity * p.product.discounted_price)
        amount +=tempamount
      total_amount = amount + shipping_amount
  else:
    product = Product.objects.get(pk = productId)
    cart_items = []
    total_amount = product.discounted_price + shipping_amount
    direct_buy = True

    data = {
    'total_amount' : amount + shipping_amount,
    }
  print(direct_buy)
  context = {
  'user_address' : user_address,
  'cart_items' : cart_items,
  'total_amount' : total_amount,
  'direct_buy' : direct_buy,
  'product' : product
  }
  return render(request, 'app/checkout.html', context)
 return redirect('/accounts/login')

def payment_done(request, productId = None):
 usr = request.user
 custid = request.GET.get('custid')
 user_address = Customer.objects.get(id = custid)
 if productId is None:
  cart_product = Cart.objects.filter(user=usr)
  for c in cart_product:
    OrderPlaced(user = usr, customer = user_address, product = c.product, quantity = c.quantity).save()
    c.delete()
 else:
  product = Product.objects.get(pk = productId)
  OrderPlaced(user= usr, customer = user_address, product = product, quantity = 1).save()
 return redirect('/orders')


def search_product(request):
 product_searched_for = request.GET.get('search-product')
 products = Product.objects.filter(brand__icontains = product_searched_for)
 context = {
  'product_searched_for' : product_searched_for,
  'products' : products
 }
 return render(request, 'app/search_prod.html', context)