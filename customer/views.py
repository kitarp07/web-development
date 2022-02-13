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
