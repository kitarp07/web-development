from random import choice
from unicodedata import category
from django.shortcuts import render
from products.models import *

# Create your views here.
def product_detail(request, pk):
    product = Products.objects.get(id=pk)
    choice = product.category
    
    related_products = Products.objects.filter(category= choice).exclude(pk = product.id)
    context = {'product': product, 'relatedProducts': related_products}
    return render(request, 'product/productdetail.html', context)