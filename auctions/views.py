from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid, Comment, Category, Watchlist


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(closed=False),
        "heading": "Active Listings"
    })


def closed_listings(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(closed=True),
        "heading": "Closed Listings"
    })


def categories(request):
    # Returns category list
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
    })

def category(request, category_id):
    # Returns listings in a category
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(category_id=category_id, closed=False),
        "heading": "Category: " + Category.objects.get(pk=category_id).name
    })


@login_required
def watchlist(request):
    return render(request, "auctions/index.html", {
        "listings": [l.listing for l in Watchlist.objects.filter(user_id=request.user.id)],
        "heading": "Watched Listings"
    })


@login_required
def add_watchlist(request, listing_id):
    """ Check the watchlist, add/remove item and return current state to JS """
    watched = Watchlist.objects.filter(user=request.user, listing_id=listing_id).first()
    if watched:
        Watchlist.objects.get(pk=watched.id).delete()
        return JsonResponse(True, safe=False)
    else:
        Watchlist.objects.create(listing_id=listing_id, user=request.user)
        return JsonResponse(False, safe=False)


@login_required
def create_listing(request):
    if request.method == "POST":
        image_file = request.FILES.get("image_file", None)
        image_url = request.POST.get("image_url", None)
        name = request.POST["name"]
        description = request.POST["description"]
        category = request.POST.get("category", None)
        price = (request.POST["price"])
        listing = Listing.objects.create(
                user=request.user,
                name=name,
                description=description,
                category=category,
                image_file=image_file,
                image_url=image_url)
        Bid.objects.create(user=request.user, listing=listing, price=price)
        return HttpResponseRedirect(reverse("listing", args=[listing.id]))
    return render(request, "auctions/create.html", {
        "categories": Category.objects.all(),
    })


@login_required
def close_listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    if request.method == "POST":
        if request.user.id != listing.user_id:
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "watched": listing.in_watchlist.filter(user_id=request.user.id).first(),
                "message": "You cannot close this listing"
            })
        listing.closed = True
        listing.save(update_fields=['closed'])
    return HttpResponseRedirect(reverse("listing", args=[listing_id]))


def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "watched": listing.in_watchlist.filter(user_id=request.user.id).first()
    })


@login_required
def bid(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        price = float(request.POST["price"])
        if price < listing.top_bid().price:
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "watched": listing.in_watchlist.filter(user_id=request.user.id).first(),
                "message": "You bid cannot be lower than current price"
            })
        Bid.objects.create(user=request.user, listing=listing, price=price)
        return HttpResponseRedirect(reverse("listing", args=[listing_id]))


@login_required
def comment(request):
    if request.method == "POST":
        listing_id = request.POST["listing_id"]
        text = request.POST["text"]
        Comment.objects.create(user=request.user, text=text, listing_id=listing_id)
        return HttpResponseRedirect(reverse("listing", args=[listing_id]))


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
