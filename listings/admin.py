from django.contrib import admin
from .models import Listing, Booking, Review


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'location', 'created_at']
    search_fields = ['title', 'location']
    list_filter = ['location', 'property_type', 'created_at']
    ordering = ['created_at']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['listing', 'renter', 'start_date', 'end_date', 'is_confirmed']
    search_fields = ['listing__title', 'renter__username']
    list_filter = ['is_confirmed', 'start_date', 'end_date']
    ordering = ['start_date']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['listing', 'user', 'rating', 'created_at']
    search_fields = ['listing__title', 'user__username']
    list_filter = ['rating', 'created_at']
    ordering = ['created_at']
