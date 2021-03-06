from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    id = models.AutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=200,blank=True, null=False)
    email = models.CharField(max_length=200,blank=True, null=False)
    phone = models.CharField(max_length=10,blank=True, null=False)
    username = models.CharField(max_length=100,blank=True, null=False)
    password = models.CharField(max_length=30,blank=True, null=False)
    

    class Meta:
        db_table = "customer"

    def __str__(self):
        return self.name

