from django.contrib.auth.models import AbstractUser
from django.db import models


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class User(AbstractUser):

    def watching_listings(self):
        # Returns the number of returns number of items user is watching
        return self.watching.count()

    pass


class Category(models.Model):
    name = models.CharField(max_length=64)
    # parent = models.ForeignKey(Category, on_delete=models.PROTECT,
    #         related_name="children")

    def __str__(self):
        return f"{self.name}"


class Listing(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=1900)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    closed = models.BooleanField(default=False)
    # image = models.ImageField(upload_to=user_directory_path)
    category = models.ForeignKey(Category, on_delete=models.PROTECT,
            related_name="listings")
    user = models.ForeignKey(User, on_delete=models.CASCADE,
            related_name="listings")

    def top_bid(self):
        # Returns the highest bid associated with the listing
        return self.bids.order_by("price").last()

    def bids_count(self):
        # Returns the number of bids associated with the listing
        return self.bids.count()

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

