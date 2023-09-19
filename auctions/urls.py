from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path('create_listing/', views.create_listing, name="create-listing"),
    path('categories/', views.categories, name="categories"),
    path('categories/<int:category_id>/', views.listings_by_category, name="listings-by-category"),
    path('listing/<int:listing_id>/', views.listing, name="listing"),
    path('add_to_wathclist/<int:listing_id>', views.add_to_watchlist, name="add-to-watchlist"),
    path('remove_from_watchlist/<int:listing_id>', views.remove_from_watchlist, name="remove-from-watchlist"),
    path('watchlists/', views.watchlists, name="watchlists"),
    path('listing/<int:listing_id>/place_bid/', views.place_bid, name="place-bid"),
    path('listing/<int:listing_id>/close_auction/', views.close_auction, name="close-auction"),
    path('closed_listings/', views.closed_listings, name="closed-listings"),
    path('listing/<int:listing_id>/add_comment/', views.add_comment, name="add-comment"),
]
