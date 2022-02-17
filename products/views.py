import imp
from django.shortcuts import render
from products.models import *
from booking.models import *
from customer.models import *


# Create your views here.
def product_detail(request, pk):
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
    product = Products.objects.get(id=pk)
    choice = product.category
    
    related_products = Products.objects.filter(category= choice).exclude(pk = product.id)
    context = {'product': product, 'relatedProducts': related_products, 'items': items,
               'order': order, 'cartItems': cartItems}
    return render(request, 'product/productdetail.html', context)