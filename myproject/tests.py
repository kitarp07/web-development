
from django.test import TestCase, SimpleTestCase, Client
from django.urls import reverse, resolve
from pages.views import *
from booking.views import *
from products.views import *
from owner.views import *
from products.models import *
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
        logged_in = client.login(username="username", password="password")

        customer = Customer.objects.create(
            user=user,
            name='full name',
            email='test@email.com',
            phone='918181818',
            username='username',
            password='password'
        )
        url = reverse('dash')
        response = client.get(url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/adminCustomer.html')

    def test_update_customer(self):
        user = User.objects.create(username="username")
        user.set_password('password')
        user.save()
        client = Client()
        logged_in = client.login(username="username", password="password")

        customer = Customer.objects.create(
            user=user,
            name='full name',
            email='test@email.com',
            phone='918181818',
            username='username',
            password='password'
        )

        url = reverse('update-customer', args=[customer.id])
        response = client.post(url, {
            'user': user,
            'name' : 'new full name',
            'email':'test@email.com',
            'phone' :'918181818',
            'username' :'username',
            'password': 'password'

        })
        
        customer.refresh_from_db()
    

        
        self.assertEquals(response.status_code, 302)
        self.assertEquals(customer.name, 'new full name')
        self.assertRedirects(response, '/dashboard/')

    
    
    def test_delete_customer(self):
        user = User.objects.create(username="username")
        user.set_password('password')
        user.save()
        client = Client()
        logged_in = client.login(username="username", password="password")

        customer = Customer.objects.create(
            user=user,
            name='full name',
            email='test@email.com',
            phone='918181818',
            username='username',
            password='password'
        )

        url = reverse('delete-customer', args=[customer.id])
        response = client.post(url)
        customer = Customer.objects.create(
            user=user,
            name='full name',
            email='test@email.com',
            phone='918181818',
            username='username',
            password='password'
        )
        print(response.status_code)
      
        
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/dashboard/')

    def test_register(self):
        user = User.objects.create(username="username")
        user.set_password('password')
        user.save()
        client = Client()
        loggged_in = client.login(username="username", password="password")

        url = reverse('register')
        response = client.post(url, {
            'name': 'first name',
            'email': 'test email',
            'address': 'test adr',
            'phone': 'phone',
            'username': 'username22',
            'password': 'password'
        })
        print(response)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/register/complete')

    def test_product_dashboard(self):
        user = User.objects.create(username="username")
        user.set_password('password')
        user.save()
        client = Client()
        logged_in = client.login(username="username", password="password")
        
        customer = Customer.objects.create(
            user=user,
            name='full name',
            email='test@email.com',
            phone='918181818',
            username='username',
            password='password'
        )
        url = reverse('products')
        response = client.get(url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/adminProduct.html')

    def test_update_product(self):
        user = User.objects.create(username="username")
        user.set_password('password')
        user.save()
        client = Client()
        logged_in = client.login(username="username", password="password")
        customer = Customer.objects.create(
            user=user,
            name='full name',
            email='test@email.com',
            phone='918181818',
            username='username',
            password='password'
        )
        category = Category.objects.create(name='new cat')
        c_id = category.id
        product = Products.objects.create(
            title='product title',
            author='product author',
            description ='product description',
            price = 100,
            category = category
        )

        url = reverse('update-product', args=[product.id])
        response = client.post(url, {
            'title':'new product title',
            'price': 1200,
            'author':'new product author',
            'description': 'new product description',
            'category': category.id

        })
        
        product.refresh_from_db()
    

        
        self.assertEquals(response.status_code, 302)
        self.assertEquals(product.title, 'new product title')
        self.assertEquals(product.author, 'new product author')
        self.assertRedirects(response, '/products/')

    
    
    def test_delete_product(self):
        user = User.objects.create(username="username")
        user.set_password('password')
        user.save()
        client = Client()
        logged_in = client.login(username="username", password="password")
        customer = Customer.objects.create(
            user=user,
            name='full name',
            email='test@email.com',
            phone='918181818',
            username='username',
            password='password'
        )
        product = Products.objects.create(
            title='product title',
            author='product author',
            description ='product description',
            price = 100
        )

        url = reverse('delete-product', args=[product.id])
        response = client.post(url)
        print(response.status_code)
      
        
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/products/')
    
    def test_adminCheckout(self):
        user = User.objects.create(username="username")
        user.set_password('password')
        user.save()
        client = Client()
        logged_in = client.login(username="username", password="password")

        customer = Customer.objects.create(
            user=user,
            name='full name',
            email='test@email.com',
            phone='918181818',
            username='username',
            password='password'
        )

        url = reverse('admin-checkout')
        response = client.get(url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/adminCheckout.html')

    def test_addOrder(self):
        user = User.objects.create(username="username")
        user.set_password('password')
        user.save()
        client = Client()
        logged_in = client.login(username="username", password="password")

        
        customer = Customer.objects.create(
            user=user,
            name='full name',
            email='test@email.com',
            phone='918181818',
            username='username',
            password='password'
        )

        product = Products.objects.create(
            title='product title',
            author='product author',
            description ='product description',
            price = 100
        )

        url = reverse('create-order')
        response = client.post(url, {
             'customer':customer.id,
             'item': product.id,
             'status': 'Pending',
             'quantity': 5,
             'address':'test address',
             'city': 'test city',
             


        })
        
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/admincheckout/')
    
    def test_updateOrder(self):
        user = User.objects.create(username="username")
        user.set_password('password')
        user.save()
        client = Client()
        logged_in = client.login(username="username", password="password")

        
        customer = Customer.objects.create(
            user=user,
            name='full name',
            email='test@email.com',
            phone='918181818',
            username='username',
            password='password'
        )

        product = Products.objects.create(
            title='product title',
            author='product author',
            description ='product description',
            price = 100
        )
        order = Order.objects.create(customer=customer, status='Pending', order_id=datetime.datetime.now().timestamp(), order_placed=False)
        order.save()
        orderproduct = OrderProduct.objects.create(order=order,
        item=product, quantity = 10)
        orderproduct.save()
        shipping = Checkout.objects.create(customer=customer,
        order=order, city='test city', address= 'test address')
        shipping.save()
        url = reverse('update-checkout', args=[orderproduct.id])
        response = client.post(url, {
             'customer':customer.id,
             'item': product.id,
             'status': 'In Process',
             'quantity': 5,
             'address':'updated address',
             'city': 'updated city',
            
        })
        order.refresh_from_db()
        orderproduct.refresh_from_db()
        shipping.refresh_from_db()
        
        self.assertEquals(response.status_code, 302)
        self.assertEquals(shipping.address, 'updated address')
        self.assertEquals(orderproduct.quantity, 5)
        self.assertRedirects(response, '/admincheckout/')

    def test_del_admin_checkout(self):
        user = User.objects.create(username="username")
        user.set_password('password')
        user.save()
        client = Client()
        logged_in = client.login(username="username", password="password")

        customer = Customer.objects.create(
            user=user,
            name='full name',
            email='test@email.com',
            phone='918181818',
            username='username',
            password='password'
        )

        product = Products.objects.create(
            title='product title',
            author='product author',
            description ='product description',
            price = 100
        )
        order, created = Order.objects.get_or_create(
            customer=customer, order_placed=False, order_id=datetime.datetime.now().timestamp())
        order.save()
        orderProduct = OrderProduct.objects.create(
             item=product, order=order, quantity=5)

      

        url = reverse('delete-checkout', args=[orderProduct.id])
        response = client.post(url)
        print(response.status_code)
      
        
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/admincheckout/')

    def test_product_detail(self):
        user = User.objects.create(username="username")
        user.set_password('password')
        user.save()
        client = Client()
        logged_in = client.login(username="username", password="password")

        customer = Customer.objects.create(
            user=user,
            name='full name',
            email='test@email.com',
            phone='918181818',
            username='username',
            password='password'
        )
        
        product = Products.objects.create(
            title='product title',
            author='product author',
            description ='product description',
            price = 100
        )
        url = reverse('product-detail', args=[product.id])
        response = client.get(url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/productdetail.html')
    
    def test_homepage(self):
        client = Client()
        url = reverse('home')
        response = client.get(url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'homepage.html')
    
    def test_customer_checkout(self):
        client = Client()
        url = reverse('checkout')
        response = client.get(url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/customer_checkout.html')