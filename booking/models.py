from django.db import models
from customer.models import *
from products.models import *


# Create your models here.
class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('In Process', 'In Process'),
        ('Completed', 'Completed'),
    )
    customer  = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(default='Pending', max_length=200, null=True, choices=STATUS)
    order_id = models.CharField(max_length=200, null=True)
    order_placed = models.BooleanField(default=False)
    

    class Meta:
        db_table = "order"

  
    @property
    def getCartTotal(self):
        ordereditems = self.orderproduct_set.all()
        total = sum([item.getTotal for item in ordereditems])
        return total
    
    @property
    def getCartItems(self):
        ordereditems = self.orderproduct_set.all()
        total = sum([item.quantity for item in ordereditems])
        return total
    
    @property
    def productsAdded(self):
        productsAdded = False
        ordereditems = self.orderproduct_set.all()
        for i in ordereditems:
            productsAdded = True
        return productsAdded
    
    def getOrderName(self):
        ordereditems = self.orderproduct_set.all()
        title = ([item.getProductName for item in ordereditems])
        return title

    

class OrderProduct(models.Model):
    item = models.ForeignKey(Products, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "orderproduct"
    def __str__(self):
        return ("Order no: " + str (self.id))
    
    @property
    def getTotal(self):
        total = self.item.price * self.quantity
        return total

    @property
    def getProductName(self):
        name = self.item.title
        return name

class Checkout(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
