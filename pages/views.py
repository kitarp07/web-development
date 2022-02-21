from datetime import datetime
from itertools import product
import json
from math import prod
from multiprocessing import context
from operator import itemgetter
import re
from turtle import title
from unicodedata import category
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group

from myproject.forms import CustomerForm, ImageForm, OrderProductForm, ProductForm, OrderForm, ShippingForm

from customer.models import Customer
from myproject.decoraters import user_authentication, admin_restrcited
from products.models import Category, Products
from booking.models import Checkout, Order, OrderProduct
import datetime
from django.core.paginator import Paginator
from django.contrib import messages


# Create your views here.

@user_authentication
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('un')
        password = request.POST.get('pw')
        print(username)
        print(password)

        
        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.success(request, "Wrong Credentials. Please try again")
        if user is not None:
            login(request, user)
            return redirect('/home/')

    return render(request, 'authenticate/login.html')


def logoutUser(request):
    logout(request)
    return redirect('login')





def new_view(request):
    return render(request, 'reg_comp.html')


def reg_view(request):
    form = CustomerForm()
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            un = form.cleaned_data['username']
            em = form.cleaned_data['email']
            pw = form.cleaned_data['password']
            cpw = request.POST.get('cpassword')

            if pw == cpw:
                user = User.objects.create_user(un, em, pw)
                user.save()

            # group = Group.objects.get(name='customer')
            # user.groups.add(group)


                customer = form.save(commit=False)
                customer.user = user
                customer.save()
                messages.success(request, 'Your account has been registered')
            elif pw != cpw:
                 messages.success(request, "Passwords don't match. Try again.")
           

    context = {'form': form}

    return render(request, 'authenticate/registration.html', context)


def showProducts_view(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        orders, created = Order.objects.get_or_create(
            customer=customer, order_placed=False)
        items = orders.orderproduct_set.all()
        cartItems = orders.getCartItems

    else:
        items = []
        order = {}
        cartItems = 0

    products = Products.objects.all()
    context = {'products': products, 'items': items, 'cartItems': cartItems}
    return render(request, 'showproduct.html', context)


def customerCheckout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        # get or create order
        order, created = Order.objects.get_or_create(
            customer=customer, order_placed=False)
        items = order.orderproduct_set.all()
        cartItems = order.getCartItems
    else:
        items = []
        order = {'getCartTotal': 0, 'getCartItems': 0}
        cartItems = order['getCartItems']

    context = {'items': items, 'order': order,
               'cartItems': cartItems, 'productsAdded': False}
    return render(request, 'cart/customer_checkout.html', context)


def base(request):
    return render(request, 'base.html')


def home(request):
    if request.user.is_authenticated:
        customer = request.user.customer
    # get or create order
        order, created = Order.objects.get_or_create(
            customer=customer, order_placed=False)
        items = order.orderproduct_set.all()
        cartItems = order.getCartItems
    else:
        items = []
        order = {'getCartTotal': 0, 'getCartItems': 0}
        cartItems = order['getCartItems']
    
    products = Products.objects.all()
    category = Category.objects.all()
    context = {'products': products, 'items': items,
               'order': order, 'cartItems': cartItems,
               'category': category,}
    return render(request, 'homepage.html', context)

def sortProducts(request, choice):
    if request.user.is_authenticated:
        customer = request.user.customer
    # get or create order
        order, created = Order.objects.get_or_create(
            customer=customer, order_placed=False)
        items = order.orderproduct_set.all()
        cartItems = order.getCartItems
    else:
        items = []
        order = {'getCartTotal': 0, 'getCartItems': 0}
        cartItems = order['getCartItems']
    category_object = Category.objects.get(name=choice)
    category_id = category_object.id
    products = Products.objects.filter(category = category_id)
   
    context = {'category': category_object,'products': products,
               'items': items,'order': order, 'cartItems': cartItems}

    return render(request, "sortProduct.html", context)



def searchProducts(request):
    if request.method == 'GET':
        search = request.GET['search']
        products = Products.objects.filter(title__icontains=search)
    context = {'products': products, 'search': search}
    return render(request, 'search.html', context)
