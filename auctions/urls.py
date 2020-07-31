from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("categories", views.categories, name="categories"),
    path("category/<str:cat_id>", views.category, name="category"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("create", views.create_listing, name="create"),
    path("listing", views.listing, name="listing"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
