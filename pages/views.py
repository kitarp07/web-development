from datetime import datetime
from itertools import product
import json
from math import prod
from multiprocessing import context
from operator import itemgetter
import re
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group

from myproject.forms import CustomerForm, ImageForm, OrderProductForm, ProductForm, OrderForm, ShippingForm

from customer.models import Customer
from myproject.decoraters import user_authentication, admin_restrcited
from products.models import Products
from booking.models import Checkout, Order, OrderProduct
import datetime
from django.core.paginator import Paginator


# Create your views here.

@user_authentication
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('un')
        password = request.POST.get('pw')
        print(username)
        print(password)

        user = authenticate(request, username=username, password=password)
        if user is not None:

            login(request, user)
            return redirect('/dashboard')

    return render(request, 'authenticate/login.html')


def logoutUser(request):
    logout(request)
    return redirect('login')


# def loginEntry(request):
#     pass
#     # user = request.POST['username']
#     # password = request.POST['password']
#     # user = authenticate(request, username=user, password=password)
#     # login(request, user)
#     # if user.is_authenticated:
#     #     return redirect('/dashboard/')
#     # else:
#     #     return('/login/')


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

            user = User.objects.create_user(un, em, pw)

            # group = Group.objects.get(name='customer')
            # user.groups.add(group)

            user.save()

            customer = form.save(commit=False)
            customer.user = user
            customer.save()
            return redirect('regcomplete')

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
    context = {'products': products, 'items': items,
               'order': order, 'cartItems': cartItems}
    return render(request, 'homepage.html', context)
