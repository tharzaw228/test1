from django.contrib import admin
from .models import Listing, Category, Bid, Comment

# Register your models here.
class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "price", "owner", "category", "bidder")

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title_category")

class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "bid_amount")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "comment")

admin.site.register(Listing, ListingAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)