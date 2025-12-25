from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    """
    Maps to users table

    Django will store the hashed passwords
    """
    email = models.EmailField(unique=True)
    profile_image = models.ImageField(upload_to="profile_images/", null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

def __str__(self):
    return self.email
    