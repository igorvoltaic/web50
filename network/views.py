from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
import json

from .models import User, Post


def index(request):
    return render(request, "network/index.html")


def profile(request, user_id):

    # # Profile must be via GET or PUT
    # if request.method != "PUT" or request.method != "GET":
    #     return JsonResponse({
    #         "error": "GET or PUT request required."
    #     }, status=400)

    user = get_object_or_404(User, pk=user_id)
    if request.method == "PUT":

        # Return error if user tries to follow self
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

def post(request, post_id):

    # Editing or liking a post must be via PUT
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)

    if not request.user.is_authenticated:
        return JsonResponse({"error": "Must be logged in."}, status=400)


    post = get_object_or_404(Post, pk=post_id)
    data = json.loads(request.body)
    if data.get("body") is not None:
        post.body = data["body"]
    if data.get("like") is not None:
        post.liked_by.add(request.user)
    if data.get("unlike") is not None:
        post.liked_by.remove(request.user)
    post.save()
    return HttpResponse(status=204)

def posts(request):

    # # Posts must be via GET or POST
    # if request.method != "POST" or request.method != "GET":
    #     return JsonResponse({
    #         "error": "GET or POST request required."
    #     }, status=400)

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
    paginator = Paginator(posts, 10)
    return JsonResponse([post.serialize(request.user) for post in posts], safe=False)


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
