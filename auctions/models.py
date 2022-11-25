from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category_name = models.CharField(max_length=20)
    
    
class Listing(models.Model):
    listing_title = models.CharField(max_length=30)
    listing_image = models.ImageField(upload_to='listing-images')
    listing_description = models.CharField(max_length=250)
    listing_starting_bid = models.DecimalField(max_digits=6,decimal_places=2)
    listing_current_price = models.DecimalField(max_digits=6,decimal_places=2)
    listing_user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing_is_active = models.BooleanField(default=True)
    listing_category = models.ForeignKey(Category, blank = True, null=True, related_name="listingCategory", on_delete=models.SET_NULL)
    listing_watchlist = models.ManyToManyField(User, blank = True, null=True, related_name="listingWatchlist")
    listing_winner = models.ForeignKey(User, blank = True, null = True, on_delete=models.SET_NULL, related_name="winner")

class Bid(models.Model):
    bid_user = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=6,decimal_places=2)
    bid_date_time = models.DateTimeField(auto_now=False, auto_now_add=True)

class Comment(models.Model):
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    comment_date_time = models.DateTimeField(auto_now=False, auto_now_add=True) 
    comment_text = models.CharField(max_length=150)