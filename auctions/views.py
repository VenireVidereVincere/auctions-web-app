from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
import pdb
from .models import User, Listing, Bid, Comment, Category

def index(request):
    listings = Listing.objects.filter(listing_is_active = True)
    return render(request, "auctions/index.html",{
        "listings": listings
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

@login_required
def create_listing(request):
    if request.method == "POST":
        try:
            newListing = Listing.objects.create(
            listing_title = request.POST["title"],
            listing_image = request.FILES["image"],
            listing_description = request.POST["description"],
            listing_starting_bid = request.POST["bid"],
            listing_current_price = request.POST["bid"],
            listing_user = request.user,
            listing_is_active = True,
            listing_category = Category.objects.get(category_name=request.POST["category"])
            )
            return HttpResponseRedirect(reverse("listing", args=(newListing.id, "Listing created successfuly!")))
        except:
            return render(request,"create-listing",{
                "error":"Please fill out all the fields before submitting."
            })
    else:
        categories = Category.objects.all()
        return render(request, "auctions/create-listing.html",{
            "categories": categories
        })

def listing(request, listing_id, message=""):
    listing = Listing.objects.get(pk=listing_id)
    listing_in_watchlist = request.user in listing.listing_watchlist.all()
    comments = Comment.objects.filter(comment_listing = listing)
    return render(request, "auctions/listing.html",{
        "listing": listing,
        "listing_in_watchlist": listing_in_watchlist,
        "message": message, 
        "comments": comments
    })

@login_required
def watchlist(request):
    currentUser = request.user
    listings = currentUser.listingWatchlist.all()
    return render(request, "auctions/watchlist.html",{
        "listings": listings
    })

def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def category(request, category_name):
    category = Category.objects.get(category_name=category_name)
    
    try:
        listings = Listing.objects.filter(listing_category = category, listing_is_active=True)
    except:
        listings = []    
    return render(request, "auctions/category.html",{
        "listings": listings
    })

@login_required
def update_watchlist(request):
    if request.method == "POST":
        listing = Listing.objects.get(pk=int(request.POST["listing_id"]))
        current_user = request.user
        if request.POST["action"] == "remove":
            listing.listing_watchlist.remove(current_user)
        elif request.POST["action"] == "add":
            listing.listing_watchlist.add(current_user)    
    return HttpResponseRedirect(reverse("listing", args=(listing.id, "Watchlist updated successfuly!")))

@login_required
def place_bid(request):
    if request.method == "POST":
        listing = Listing.objects.get(pk=request.POST["listing_id"])
        if float(request.POST["bid"]) > listing.listing_current_price:
            bid = Bid.objects.create(
                bid_listing = listing,
                bid_amount = float(request.POST["bid"]),
                bid_user = request.user
            )
            listing.listing_current_price = bid.bid_amount
            listing.listing_winner = request.user
            listing.save()
            return HttpResponseRedirect(reverse("listing", args=(listing.id, "Your bid was submitted successfully!")))
        else:
            return HttpResponseRedirect(reverse("listing", args=(listing.id, "Your bid must be higher than the current bid.")))
    return HttpResponseRedirect(reverse('login'))

@login_required
def submit_comment(request):
    if request.method == "POST":
        listing = Listing.objects.get(pk=int(request.POST["listing_id"]))
        comment = Comment.objects.create(
            comment_user = request.user,
            comment_listing = listing,
            comment_text = request.POST["comment"]
        )
        return HttpResponseRedirect(reverse("listing", args=(listing.id, "Your comment was submitted")))
    return HttpResponseRedirect(reverse('login'))

@login_required
def close_auction(request):
    if request.method == "POST":
        listing = Listing.objects.get(pk=int(request.POST["listing_id"]))
        listing.listing_is_active = False
        listing.save()
        return HttpResponseRedirect(reverse('listing', args=(listing.id, "Auction closed successfuly!")))
    return HttpResponseRedirect(reverse('login'))