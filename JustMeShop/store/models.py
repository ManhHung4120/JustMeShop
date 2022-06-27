from email.mime import image
from msilib.schema import Property
from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, null = True, blank = True)
    name = models.CharField(max_length= 200, null = True)
    email = models.CharField(max_length= 200, null = True)   
    
    def __str__(self):
        return self.name
    
class Product(models.Model):    
    name = models.CharField(max_length= 200, null = True)
    price = models.FloatField()   
    image = models.ImageField(null = True, blank = True)
    
    def __str__(self):
        return self.name  
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url 
    
    
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.SET_NULL, blank= True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null = True, blank = False)
    transaction_id = models.CharField(max_length= 200 , null = True)
    
    def __str__(self):
        return str(self.id)
                  
    @property
    def total_all(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total_item for item in orderitems])
        return total
    
    @property
    def total_item(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quatity for item in orderitems])
        return total
    
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete = models.SET_NULL, blank= True, null= True)
    order = models.ForeignKey(Order, on_delete = models.SET_NULL, blank= True, null= True)
    quatity = models.IntegerField(default=0, null = True, blank = True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    @property
    def get_total_item(self):
        total = self.product.price * self.quatity
        return total
    
    
class Shipping(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank = True , null= True)
    order = models.ForeignKey(Order, on_delete = models.SET_NULL, blank= True, null=  True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length= 200, null= True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address 