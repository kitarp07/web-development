from unicodedata import category
from django.shortcuts import render
from datetime import datetime
from itertools import product
import json
from math import prod
from multiprocessing import context
from operator import itemgetter
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group

from myproject.forms import CustomerForm, ImageForm, OrderProductForm, ProductForm, OrderForm, ShippingForm

from customer.models import Customer
from myproject.decoraters import user_authentication, admin_restrcited
from products.models import Products, Category
from booking.models import Checkout, Order, OrderProduct
import datetime
from django.core.paginator import Paginator

# Create your views here.

@login_required(login_url='login')
# @admin_restrcited
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
    return render(request, 'admin/updateCustomer.html', context)

@login_required(login_url='login')
# @admin_restrcited
def deleteCustomer(request, pk):
    customer = Customer.objects.get(id=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('/dashboard/')
    context = {'customer': customer}
    return render(request, 'admin/deleteCustomer.html', context)


@login_required(login_url='login')
# @admin_restrcited
def adminCustomer_view(request):
    customer = Customer.objects.all()
    paginator = Paginator(customer, 5)
    page_no = request.GET.get('page')
    page = paginator.get_page(page_no)
    context = {'customers': page}
    return render(request, 'admin/adminCustomer.html', context)

# @login_required(login_url='login')
# @admin_restrcited

@login_required(login_url='login')
# @admin_restrcited
def adminProduct_view(request):
    product = Products.objects.all()
    paginator = Paginator(product, 5)
    page_no = request.GET.get('page')
    page = paginator.get_page(page_no)
    context = {'products': page}
    return render(request, 'admin/adminProduct.html', context)

# @login_required(login_url='login')
# @admin_restrcited
def create_products_view(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/products/')
    category = Category.objects.all()
    context = {'form': form, 'category': category}
    return render(request, 'admin/createProduct.html', context)

@login_required(login_url='login')
# @admin_restrcited
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
        category_id = request.POST.get('category')
        category_obj = Category.objects.get(id=category_id)
        product.category = category_obj
        product.save()

        imageform.save()
        return redirect('/products/')
    category = Category.objects.all()
    context = {'form': form, 'product': product, 'imageform': imageform, 'category': category}
    return render(request, 'admin/updateproduct.html', context)

@login_required(login_url='login')
# @admin_restrcited
def deleteProduct(request, pk):
    product = Products.objects.get(id=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('/products/')
    context = {'product': product}
    return render(request, 'admin/deleteproduct.html', context)


def orders_view(request):
    orders = Order.objects.all()
    context = {'orders': orders}
    return render(request, 'order/order.html', context)

@login_required(login_url='login')
# @admin_restrcited
def createOrder(request):
    orderform = OrderForm()
    orderproductform = OrderProductForm()
    checkoutform = ShippingForm()
    customer = Customer.objects.all()
    product = Products.objects.all()
    if request.method == 'POST':
        orderform = OrderForm(request.POST)
        orderproductform = OrderProductForm(request.POST)
        checkoutform = ShippingForm(request.POST)
        orderCustomer = request.POST.get('customer')
        orderProduct = request.POST.get('item')
        orderStatus = request.POST.get('status')
        orderCustomer_object = Customer.objects.get(id=orderCustomer)
        orderProduct_object = Products.objects.get(id=orderProduct)
        order, created = Order.objects.get_or_create(
            customer=orderCustomer_object, order_placed=False, status=orderStatus, order_id=datetime.datetime.now().timestamp())
        order.save()
        order.order_placed = True
        orderQuantity = request.POST.get('quantity')
        orderProduct, created = OrderProduct.objects.get_or_create(
            order=order, item=orderProduct_object, quantity=orderQuantity)
        orderProduct.save()
        checkoutAddress = request.POST.get('address')
        checkoutCity = request.POST.get('city')
        Checkout.objects.create(
            customer=orderCustomer_object,
            order=order,
            city=checkoutCity,
            address=checkoutAddress,

        )
        return redirect('/admincheckout/')
    context = {'customer': customer, 'product': product}
    return render(request, 'admin/createOrder.html', context)

@login_required(login_url='login')
# @admin_restrcited
def updateOrder(request, pk):
    orderform = OrderForm()
    orderproductform = OrderProductForm()
    checkoutform = ShippingForm()
    customer = Customer.objects.all()
    product = Products.objects.all()
    orderProduct = OrderProduct.objects.get(id=pk)
    order = Order.objects.get(id=orderProduct.order.id)
    shipping = Checkout.objects.get(order=order.id)
    orderProduct_item = Products.objects.get(id=orderProduct.item.id)   
    orderCustomer_object = Customer.objects.get(id=order.customer.id) 
    if request.method == 'POST':
        orderform = OrderForm(request.POST)
        orderproductform = OrderProductForm(request.POST)
        checkoutform = ShippingForm(request.POST)
        orderCustomer = request.POST.get('customer')
        orderItem = request.POST.get('item')
        orderStatus = request.POST.get('status')
        updateCustomer_object = Customer.objects.get(id=orderCustomer)
        updateProduct_object = Products.objects.get(id=orderItem)
        order.customer = updateCustomer_object
        order.status = orderStatus
        order.save()
        orderQuantity = request.POST.get('quantity')
        orderProduct.quantity = orderQuantity
        orderProduct.item = updateProduct_object
        orderProduct.save()
        checkoutAddress = request.POST.get('address')
        checkoutCity = request.POST.get('city')
        shipping.address = checkoutAddress
        shipping.city = checkoutCity
        shipping.save()
       
        return redirect('/admincheckout/')
    context = {'customer': customer, 'product': product, 
    'orderProduct': orderProduct,
    'order': order,
    'shipping': shipping,
    'orderProduct_item': orderProduct_item, 
    'orderCustomer': orderCustomer_object}
    return render(request, 'admin/updateOrder.html', context)

@login_required(login_url='login')
# @admin_restrcited
def adminCheckout(request):
    checkout = Checkout.objects.all()
    orders_customer = Order.objects.all()
    orders_products = OrderProduct.objects.all()
    paginator = Paginator(orders_products, 5)
    page_no = request.GET.get('page')
    page = paginator.get_page(page_no)
    context = {'checkout': checkout, 'orders_customer': orders_customer,
               'orders_products': page}
    return render(request, 'admin/adminCheckout.html', context)

@login_required(login_url='login')
# @admin_restrcited
def deleteCheckedoutOrder(request, pk):
    order = OrderProduct.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()

        return redirect('/admincheckout/')
    context = {'product': product}
    return render(request, 'admin/deleteproduct.html', context)