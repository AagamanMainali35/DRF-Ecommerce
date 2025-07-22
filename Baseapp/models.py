from django.db import models 
from django.contrib.auth.models import User 
class Profile(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_id = models.CharField(max_length=50, unique=True, default='#000')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    role = models.CharField(max_length=20, default='customer')
    def __str__(self):
        return f'Profile of  "{self.user.username}" '
   
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sold_count = models.PositiveIntegerField(default=0)
    dicount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    dicount_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    def __str__(self):
        return self.name
    
class Cart(models.Model):
    customer=models.OneToOneField(User,verbose_name="Related_User",on_delete=models.CASCADE)
    totalAmount=models.PositiveIntegerField()
    def __str__(self):
        return self.customer.username

class Cart_item(models.Model):
    prodcut_instance=models.ForeignKey(Product,on_delete=models.CASCADE)
    cart_instance=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='cart_items')
    quantity = models.PositiveIntegerField()
    
    def __str__(self):
        return f'{self.prodcut_instance.name}-{self.cart_instance.customer.username} '  
    

    
        
