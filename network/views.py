from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
import json

from .models import User, Post


def index(request):
    return render(request, "network/index.html")


def profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == "PUT":

        # Return error if user trie to follow self
        if not user.valid_follow(request.user) or not request.user.is_authenticated:
            return JsonResponse({"message": "invalid follower."},
                                status=400)

        # Add or remove a follower
        if request.user.id not in [user.id for user in user.followers.all()]:
            user.followers.add(request.user)
            user.save()
            return JsonResponse({"message": "User follower added."},
                                status=201)
        else:
            user.followers.remove(request.user)
            user.save()
            return JsonResponse({"message": "User follower removed."},
                                status=201)

    data = {
        "followers_count": user.followers.count(),
        "follow_count": user.follow.count(),
        "followers_names": [user.username for user in user.followers.all()],
        "follow_names": [user.username for user in user.follow.all()]
        }
    return JsonResponse(data)


def posts(request):
    if request.method == "POST":

        # Create a new post
        data = json.loads(request.body)
        body = data.get("body", "")
        post = Post(
            user=request.user,
            body=body
        )
        post.save()
        return JsonResponse({"message": "Post successfully created."},
                            status=201)

    # Get all posts from all users, with the most recent posts first
    posts = Post.objects.order_by("-timestamp")
    return JsonResponse([post.serialize(request.user) for post in posts],
                        safe=False)


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
