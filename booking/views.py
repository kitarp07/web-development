import imp
from django.shortcuts import render
from .models import *
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