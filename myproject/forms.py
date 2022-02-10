from calendar import c
import imp
from pyexpat import model
from attr import fields
from django.forms import ModelForm
from customer.models import Customer
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import AbstractUser

from products.models import Products
from booking.models import *

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

class ProductForm(ModelForm):
    class Meta:
        model = Products
        fields =('__all__')
class ImageForm(ModelForm):
    class Meta:
        model = Products
        fields = ('image',)

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ('__all__')

