from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    title_category = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.title_category}"

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    image = models.URLField()
    price = models.FloatField()
    active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category,blank=True, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.title}"
