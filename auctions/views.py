from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import  BidForm, CommentForm, ListingForm
from django.contrib import messages

from .models import User, Category, Bid, Listing



def index(request):
    listings = Listing.objects.filter(active=True)
    context = {
        "listings" : listings
    }
    return render(request, "auctions/index.html", context)

def closed_listings(request):
    listings = Listing.objects.filter(active=False)
    context = {
        "listings" : listings
    }
    return render(request, "auctions/closed_listings.html", context)


def listing(request, listing_id):
    # Use get_object_or_404 to retrieve a single listing or return a 404 error if not found
    listing = get_object_or_404(Listing, pk=listing_id,)
    user = request.user
    isWatchlist =  user in listing.watchlist.all()
    bid_form = BidForm()
    comment_form = CommentForm()
    if not listing.active and user == listing.bidder.user:
        messages.success(request, 'Congratulations! You won the auction!!!!!!!!!!!!!!!')
    return render(request, "auctions/listing.html", {
        "listing" : listing,
        "isWatchlist" : isWatchlist,
        "bid_form" : bid_form,
        "comment_form" : comment_form
    })

def add_comment(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id,)
    user = request.user
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = user
            comment.save()
            listing.comments.add(comment)
            return redirect('listing', listing_id=listing_id)

def close_auction(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    user = request.user
    if request.method == 'POST':
        if user == listing.owner:
            listing.active = False
            listing.save()
            return redirect('listing', listing_id=listing_id) 

    

def place_bid(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    if request.method =="POST":
        form = BidForm(request.POST)
        if form.is_valid():
            bid = form.save(commit=False)
            bid.listing = listing
            bid.user = request.user  # Associate the bid with the logged-in user
            if  bid.bid_amount > listing.price:
                bid.save()
                listing.price = bid.bid_amount
                listing.bidder = bid
                listing.save()
                messages.success(request, 'Bid placed successfully!')
                return HttpResponseRedirect(reverse("listing", args=(listing_id, )))
            else:
                messages.error(request, 'Bid amount must be greater than the current price.')

                # Redirect back to the listing page with the error message
                return HttpResponseRedirect(reverse("listing", args=(listing_id, )))
        else:
            messages.error(request, 'Invalid bid. Please correct the form.')
    else:
        form = BidForm()
        return render(request, "auctions/listing.html", {
            "form" : form
        })

@login_required
def watchlists(reqeust):
    watchlists = reqeust.user.watchlists.all()
    return render(reqeust, "auctions/watchlists.html", {
        "watchlists" : watchlists
    })

def add_to_watchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    user = request.user
    listing.watchlist.add(user)
    return HttpResponseRedirect(reverse("listing", args=(listing_id, )))

def remove_from_watchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    user = request.user
    listing.watchlist.remove(user)
    return HttpResponseRedirect(reverse("listing", args=(listing_id, )))

def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories" : categories
    })

def listings_by_category(request, category_id):
    category = Category.objects.get(pk=category_id)
    listings = Listing.objects.filter(category=category)
    return render(request, "auctions/listings_by_category.html", {
        "listings" : listings,
        'category' : category
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
    return HttpResponseRedirect(reverse("login"))


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
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.active = True
            listing.save()
            return redirect('listing', listing_id=listing.pk)
    else:
        form = ListingForm()

    return render(request, 'auctions/create_listing.html', {'form': form})
