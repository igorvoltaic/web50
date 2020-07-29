from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"


class Listing(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=1900)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    # img =
    category = models.ForeignKey(Category, on_delete=models.PROTECT,
            related_name="listings")
    user = models.ForeignKey(User, on_delete=models.CASCADE,
            related_name="listings")

    def __str__(self):
        return f"Listing {self.id} by {self.user.username}, created {self.created}"


class Bid(models.Model):
    price = models.DecimalField(max_digits=18, decimal_places=2)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE,
            related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE,
            related_name="bids")

    def __str__(self):
        return f"Bid {self.id}: ${self.price}usd on listing {self.listing.name}"


class Comment(models.Model):
    text = models.CharField(max_length=200)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE,
            related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE,
            related_name="comments")

    def __str__(self):
        return f"Comment {self.id} by {self.user.username}"


class Watchlist(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE,
            related_name="in_watchlists")
    user = models.ForeignKey(User, on_delete=models.CASCADE,
            related_name="watching_items")

