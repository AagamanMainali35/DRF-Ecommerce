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
