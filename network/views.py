from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
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
    if request.method not in ["PUT", "GET"]:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)

    user = get_object_or_404(User, pk=user_id)

    valid_follow = False
    if user.valid_follow(request.user) and request.user.is_authenticated:
        valid_follow = True

    is_followed = False
    if request.user.id in [user.id for user in user.followers.all()]:
        is_followed = True

    if request.method == "PUT":

        # Return error if user tries to follow self
        if not valid_follow:
            return JsonResponse({"message": "invalid follower."},
                                status=400)

        # Add or remove a follower
        if not is_followed:
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
        "username": user.username,
        "is_followed": is_followed,
        "valid_follow": valid_follow,
        "followers_count": user.followers.count(),
        "follow_count": user.follow.count(),
        "follows": [{"username": u.username, "id": u.id} for u in user.follow.all()],
        "followers": [{"username": u.username, "id": u.id} for u in user.followers.all()],
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

    # Posts must be via GET or POST
    if request.method not in ["POST", "GET"]:
        return JsonResponse({
            "error": "GET or POST request required."
        }, status=400)

    if request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse({"message": "Please login."},
                                status=400)

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

    page_num = int(request.GET["page"])
    try:
        following = int(request.GET["follow"])
    except KeyError:
        following = False
    try:
        profile = int(request.GET["profile"])
    except KeyError:
        profile = False

    # Get posts from followed users, with the most recent posts first
    if following:
        if not request.user.is_authenticated:
            return JsonResponse({"message": "Please login."},
                                status=400)
        posts = Post.objects.filter(user__followers__id=request.user.id).order_by("-timestamp")
    # Get all posts from a certain user users, with the most recent posts first
    elif profile:
        posts = Post.objects.filter(user_id=profile).order_by("-timestamp")
    # Get all posts from all users, with the most recent posts first
    else:
        posts = Post.objects.order_by("-timestamp")

    paginator = Paginator(posts, 10)
    if not page_num:
        page_num = 1
    page = paginator.page(page_num)
    data = {
        "posts": [post.serialize(request.user) for post in page.object_list],
        "has_next": page.has_next(),
        "has_prev": page.has_previous()
    }
    return JsonResponse(data)


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
            return HttpResponseRedirect("/#/login")  # redirect to vue route
            # TODO: login failed message. something like redirect to '/#/login/failed'
            # with additional prop to show the message
    else:
        return HttpResponseRedirect("/#/login")  # redirect to vue route


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
            return HttpResponseRedirect("/#/register")  # redirect to vue route
            # TODO: login failed message. something like redirect to '/#/register/failed'
            # with additional prop to show the message "Username already taken."
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponseRedirect("/#/register")  # redirect to vue route
