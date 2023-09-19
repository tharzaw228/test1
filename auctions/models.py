from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    title_category = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.title_category}"

class Bid(models.Model): 
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    bid_amount= models.FloatField()
    
    def __str__(self):
        return f"{ self.bid_amount } by { self.user }"
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    image = models.URLField()
    price = models.FloatField()
    active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category,blank=True, on_delete=models.CASCADE, null=True)
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="watchlists")
    bidder = models.ForeignKey(Bid,on_delete=models.CASCADE, blank=True, null=True)
    comments = models.ManyToManyField(Comment, blank=True,related_name="listing_comments")
    def __str__(self):
        return f"{self.title}"





