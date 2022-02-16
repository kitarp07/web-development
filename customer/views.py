from django.shortcuts import render
from customer.models import Customer
# Create your views here.
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


def customer_view(request):
    customer = Customer.objects.all()
    context={'customers': customer}
    return render(request, "file.html", context)

def changePassword(request, pk):
    customer = Customer.objects.get(id=pk)
    user = request.user
    if request.method=='POST':
        old_password = request.POST.get('oldpassword')
        new_password = request.POST.get('newpassword')
        confirm_password = request.POST.get('confirm-password')
        if customer.password == old_password:
            if new_password == confirm_password:
                customer.password = new_password
                customer.save()
                user.set_password(new_password)
                user.save()
        
    return render(request, 'customer/changePassword.html')

def updateAccount(request, pk):
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
        return redirect('/home/')

    context = {'form': form, 'customer': customer}
    return render(request, 'customer/updateAccount.html', context)
