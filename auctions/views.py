from django.contrib.auth import authenticate, login, logout, get_user
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid, Comment, Category, Watchlist


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all(),
        "heading": "Active Listings"
    })


def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
    })

def category(request, category_id):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(category_id=category_id),
        "heading": "Category: " + Category.objects.get(pk=category_id).name
    })


@login_required
def watchlist(request):
    return render(request, "auctions/index.html", {
        "listings": [l.listing for l in
            Watchlist.objects.filter(user_id=get_user(request).id)],
        "heading": "Watched Listings"
    })


@login_required
def add_watchlist(request, listing_id):
    # Check the watchlist, add/remove item and return current state to JS
    watched = Watchlist.objects.filter(user_id=get_user(request).id, listing_id=listing_id)
    if watched:
        Watchlist.objects.get(pk=watched[0].id).delete()
        return JsonResponse(True, safe=False)
    else:
        watch = Watchlist(listing_id=listing_id,
                user_id=get_user(request).id)
        watch.save()
        return JsonResponse(False, safe=False)


@login_required
def create_listing(request):
    return HttpResponse('OK')


def listing(request, listing_id):
    return render(request, "auctions/listing.html", {
        "listing": Listing.objects.get(pk=listing_id)
    })


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
