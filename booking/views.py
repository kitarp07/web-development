import imp
from django.shortcuts import render
from .models import *
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


def customer_cart(request):
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
    context = { 'items': items, 'cartItems': cartItems, 'order': order}
    return render(request, 'cart/cart.html', context)
    

def updateCartData(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print(action, productId)

    customer = request.user.customer
    item = Products.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        customer=customer, order_placed=False)
    orderProduct, created = OrderProduct.objects.get_or_create(
        order=order, item=item)

    if action == 'add':
        orderProduct.quantity = (orderProduct.quantity + 1)
    elif action == 'remove':
        orderProduct.quantity = (orderProduct.quantity - 1)

    orderProduct.save()

    if orderProduct.quantity <= 0:
        orderProduct.delete()

    return JsonResponse('Item added to cart', safe=False)

def processCheckout(request):
    print(request.body)
    checkoutId = datetime.datetime.now().timestamp()
    checkoutData = json.loads(request.body)
    if request.user.customer:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, order_placed=False)
        cart_total = float(checkoutData['cart']['cart_total'])
        order.order_id = checkoutId
        print(order.getCartTotal)

        if cart_total == order.getCartTotal:
            order.order_placed = True
        order.save()

        if order.productsAdded == True:
            Checkout.objects.create(
                customer=customer,
                order=order,
                city=checkoutData['form']['city'],
                address=checkoutData['form']['address'],

            )
    else:
        print('no user')
    return JsonResponse('Order placed', safe=False)