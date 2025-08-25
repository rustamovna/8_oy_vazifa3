from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    ism = models.CharField(max_length=50, blank=True)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    code = models.CharField(max_length=6, blank=True)   # OTP kod
