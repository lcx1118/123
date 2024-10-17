from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)

class Image(models.Model):
    image_url = models.URLField(max_length=1024)

    def __str__(self):
        return self.image_url
