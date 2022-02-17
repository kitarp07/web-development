from django.db import models


# Create your models here.


class Category(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name
class Products(models.Model):
    CATEGORY= (
        ("Childrens", "Childrens"),
        ("New Arrival", "New Arrival" ),
        ("Self Help", "Self Help"),
        ("Fiction", "Fiction"),
        ("Non-Fiction", "Non-Fiction"),
        ("Health and Fitness", "Health and Fitness"),
        ("History", "History"),
        ("Popular right now", "Popular right now"),
         )

    id = models.AutoField(auto_created=True, primary_key=True)
    title = models.CharField(max_length=200, blank=True, null=False)
    price = models.FloatField(null=True)
    author = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE)



    
    @property
    def imageurl(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


    class Meta:
        db_table = "product"

    def __str__(self):
        return self.title
    

