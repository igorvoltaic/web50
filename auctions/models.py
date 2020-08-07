from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    def watching_listings(self):
        # Returns the number of returns number of items user is watching
        return self.watching.count()

    pass


class Category(models.Model):
    name = models.CharField(max_length=64)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}"


class Listing(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=1900)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    closed = models.BooleanField(default=False)
    image_url = models.URLField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT,
            related_name="listings", blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
            related_name="listings")

    def top_bid(self):
        # Returns the highest bid associated with the listing
        return self.bids.order_by("price").last()

    def __str__(self):
        return f"({self.id}) {self.name} by {self.user.username}, created {self.created}"


class Bid(models.Model):
    price = models.DecimalField(max_digits=18, decimal_places=2)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE,
            related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE,
            related_name="bids")

    def __str__(self):
        return f"Bid {self.id}: ${self.price}usd on listing {self.listing.name}"


class Comment(models.Model):
    text = models.CharField(max_length=2000)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE,
            related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE,
            related_name="comments")

    def __str__(self):
        return f"Comment {self.id} by {self.user.username}"


class Watchlist(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE,
            related_name="in_watchlist")
    user = models.ForeignKey(User, on_delete=models.CASCADE,
            related_name="watching")

