from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create-listing", views.create_listing, name="create-listing"),
    path("listing/<listing_id>", views.listing, name="listing2"),
    path("listing/<listing_id>/<message>", views.listing, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("categories/<category_name>", views.category, name="category"),
    path("update-watchlist", views.update_watchlist, name="update-watchlist"),
    path("place-bid", views.place_bid, name="place-bid"),
    path("submit-comment", views.submit_comment, name="submit-comment"),
    path("close-auction", views.close_auction, name="close-auction")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
