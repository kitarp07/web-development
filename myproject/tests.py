from re import S
from django.test import TestCase, SimpleTestCase, Client
from django.urls import reverse, resolve
from pages.views import *
from booking.views import *
from products.views import *
from owner.views import *
# Create your tests here.

class TestUrls(SimpleTestCase):
    def test_home(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func, home)

    def test_login(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func, login_view)

    def test_logout(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func, logoutUser)

    def test_reg(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func, reg_view)


    def test_adminCustomer(self):
        url = reverse('dash')
        self.assertEquals(resolve(url).func, adminCustomer_view)

    def test_addProduct(self):
        url = reverse('add-product')
        self.assertEquals(resolve(url).func, create_products_view)

    def test_adminProduct(self):
        url = reverse('products')
        self.assertEquals(resolve(url).func, adminProduct_view)

    def test_updateProduct(self):
        url = reverse('update-product', args=[1])
        self.assertEquals(resolve(url).func, updateProduct)

    def test_deleteProduct(self):
        url = reverse('delete-product', args=[1])
        self.assertEquals(resolve(url).func, deleteProduct)

    def test_deleteCustomer(self):
        url = reverse('delete-customer', args=[1])
        self.assertEquals(resolve(url).func, deleteCustomer)

    def test_createOrder(self):
        url = reverse('create-order')
        self.assertEquals(resolve(url).func, createOrder)

    def test_adminCheckout(self):
        url = reverse('admin-checkout')
        self.assertEquals(resolve(url).func, adminCheckout)

    def test_processCheckout(self):
        url = reverse('process-checkout')
        self.assertEquals(resolve(url).func, processCheckout)

    def test_deleteCheckout(self):
        url = reverse('delete-checkout', args=[1])
        self.assertEquals(resolve(url).func, deleteCheckedoutOrder)

    def test_productDetail(self):
        url = reverse('product-detail', args=[1])
        self.assertEquals(resolve(url).func, product_detail)

    def test_cart(self):
        url = reverse('cart')
        self.assertEquals(resolve(url).func, customer_cart)

    def test_checkout(self):
        url = reverse('checkout')
        self.assertEquals(resolve(url).func, customerCheckout)

    def test_update_cart_data(self):
        url = reverse('update-cart-data')
        self.assertEquals(resolve(url).func, updateCartData)

    def test_update_customer(self):
        url = reverse('update-customer', args=[1])
        self.assertEquals(resolve(url).func, updateCustomer)


class TestViews(TestCase):
    def test_customer_dashboard(self):
        user = User.objects.create(username="username")
        user.set_password('password')
        user.save()
        client = Client()
        loggged_in = client.login(username="username", password="password")

        url = reverse('dash')
        response = client.get(url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/adminCustomer.html')

    def test_customer(self):
        # user = User.objects.create(username="username")
        # user.set_password('password')
        # user.save()
        client = Client()
        # loggged_in = client.login(username="username", password="password")

        url = reverse('register')
        response = client.post(url, {
            'fname': 'first name',
            'laname': 'lastname',
            'email': 'test email',
            'address': 'test adr',
            'phone': 'phone',
            'username': 'username22',
            'password': 'password'
        })
        print(response)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/register/complete')
