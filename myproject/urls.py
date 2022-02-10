"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from unicodedata import name
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from customer.views import customer_view

from pages.views import (
login_view, 
reg_view, 
new_view, 
dashboard_view, 
create_products_view,
products_view,
logoutUser,
updateProduct,
updateCustomer,
deleteProduct,
deleteCustomer,
createOrder,
orders_view,
showProducts_view,
updateCartData,
adminCheckout,
processCheckout,
customerCheckout,
deleteCheckedoutOrder,
base,
home

)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', base),
    path('home/', home, name='home'),
    path('file/', customer_view),
    path('login/', login_view, name='login'),
    path('logout/', logoutUser, name='logout'),
    path('register/', reg_view, name='register'),
    path('register/complete', new_view, name='regcomplete'),
    path('dashboard/', dashboard_view, name='dash'),
    path('add-products/', create_products_view, name='add-product'),
    path('products/', products_view, name='products'),
    path('update-product/<int:pk>/', updateProduct, name='update-product'),
    path('delete-product/<int:pk>/', deleteProduct, name='delete-product'),
    path('update-customer/<int:pk>/', updateCustomer, name='update-customer'),
    path('delete-customer/<int:pk>/', deleteCustomer, name='delete-customer'),
    path('create-order', createOrder, name='create-order'),
    path('orders', orders_view, name='order'),
    path('showproducts', showProducts_view, name='showproduct' ),
    path('update-cart-data/', updateCartData, name='update-cart-data'),
    path('admincheckout/', adminCheckout, name='admin-checkout'),
    path('checkout-process/', processCheckout, name='process-checkout'),
    path('checkout/', customerCheckout, name='checkout'),
    path('delete-checkout/<int:pk>/', deleteCheckedoutOrder, name='delete-checkout')



   

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

