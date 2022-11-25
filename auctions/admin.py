from django.contrib import admin
from .models import Listing, User, Bid, Comment, Category

# Register your models here.
class ListingAdmin(admin.ModelAdmin):
    pass

admin.site.register(Listing, ListingAdmin)
admin.site.register(User)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Category)
