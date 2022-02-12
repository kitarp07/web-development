from datetime import datetime
import email
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

from myproject.forms import CustomerForm, ImageForm, ProductForm, OrderForm

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


def updateCustomer(request, pk):
    customer = Customer.objects.get(id=pk)
    user = request.user
    form = CustomerForm(request.POST)
    if request.method == 'POST':
        customer.name = request.POST.get('name')
        customer.email = request.POST.get('email')
        customer.phone = request.POST.get('phone')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')
        if password != customer.password:
            if username != customer.username:
                if password == confirm_password:
                    user.set_password(password)
                    customer.password = password
                user.username = username
                user.save()
                customer.username = username
        customer.save()
        return redirect('/dashboard/')

    context = {'form': form, 'customer': customer}
    return render(request, 'updateCustomer.html', context)


def deleteCustomer(request, pk):
    customer = Customer.objects.get(id=pk)
    if request.method == 'POST':
        customer.delete()
    context = {'customer': customer}
    return render(request, 'deleteCustomer.html', context)


@login_required(login_url='login')
# @admin_restrcited
def dashboard_view(request):
    customer = Customer.objects.all()
    paginator = Paginator(customer, 5)
    page_no = request.GET.get('page')
    page = paginator.get_page(page_no)
    context = {'customers': page}
    return render(request, 'customer.html', context)

# @login_required(login_url='login')
# @admin_restrcited


def products_view(request):
    product = Products.objects.all()
    paginator = Paginator(product, 5)
    page_no = request.GET.get('page')
    page = paginator.get_page(page_no)
    context = {'products': page}
    return render(request, 'product/rtable.html', context)

# @login_required(login_url='login')
# @admin_restrcited


def create_products_view(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/products/')
    context = {'form': form}
    return render(request, 'product/create.html', context)


def updateProduct(request, pk):
    product = Products.objects.get(id=pk)
    form = ProductForm(request.POST, request.FILES)
    imageform = ImageForm(request.POST, request.FILES, instance=product)
    if request.method == 'POST':
        imageform = ImageForm(request.POST, request.FILES, instance=product)
        product.title = request.POST.get('title')
        product.author = request.POST.get('author')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        product.category = request.POST.get('category')
        product.save()

        imageform.save()
        return redirect('/products/')

    context = {'form': form, 'product': product, 'imageform': imageform}
    return render(request, 'product/updateproduct.html', context)


def deleteProduct(request, pk):
    product = Products.objects.get(id=pk)
    if request.method == 'POST':
        product.delete()
        redirect('/')
    context = {'product': product}
    return render(request, 'product/deleteproduct.html', context)


def orders_view(request):
    orders = Order.objects.all()
    context = {'orders': orders}
    return render(request, 'order/order.html', context)


def createOrder(request):
    form = OrderForm()
    customer = Customer.objects.all()
    product = Products.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(request, 'order/createorder.html', context)


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


def adminCheckout(request):
    checkout = Checkout.objects.all()
    orders_customer = Order.objects.all()
    orders_products = OrderProduct.objects.all()
    paginator = Paginator(orders_products, 5)
    page_no = request.GET.get('page')
    page = paginator.get_page(page_no)
    context = {'checkout': checkout, 'orders_customer': orders_customer,
               'orders_products': page}
    return render(request, 'order/checkout.html', context)


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
    return render(request, 'customer_checkout.html', context)


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


def deleteCheckedoutOrder(request, pk):
    order = OrderProduct.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()

        redirect('/')
    context = {'product': product}
    return render(request, 'product/deleteproduct.html', context)


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
    context = {'products': products, 'items' : items, 'order': order, 'cartItems': cartItems}
    return render(request, 'homepage.html', context)
