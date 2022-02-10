from re import S
from django.test import TestCase, SimpleTestCase, Client
from django.urls import reverse, resolve
from pages.views import *
# Create your tests here.


class TestUrls(SimpleTestCase):
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
        self.assertTemplateUsed(response, 'dashboard.html')

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

        