from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add-watchlist/<int:listing_id>", views.add_watchlist, name="add-watchlist"),
    path("categories", views.categories, name="categories"),
    path("category/<int:category_id>", views.category, name="category"),
    path("close/<int:listing_id>", views.close_listing, name="close"),
    path("closed_listings", views.closed_listings, name="closed_listings"),
    path("comment", views.comment, name="comment"),
    path("create", views.create_listing, name="create"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("watchlist", views.watchlist, name="watchlist")
]
