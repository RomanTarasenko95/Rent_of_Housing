from django.core.exceptions import ValidationError
from django.conf import settings
from django.db import models
from django.utils import timezone


class Listing(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    number_of_rooms = models.IntegerField()
    property_type = models.CharField(max_length=50, choices=[('apartment', 'Квартира'), ('house', 'Дом'), ('studio', 'Студия')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class SearchHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=255)
    searched_at = models.DateTimeField(auto_now_add=True)


class ViewHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)


class Booking(models.Model):
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE, related_name='bookings')
    renter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    start_date = models.DateField()
    end_date = models.DateField()
    is_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['listing', 'start_date', 'end_date'],
                name='unique_booking_for_dates'
            )
        ]
        ordering = ['start_date']

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError('Дата начала не может быть позже даты окончания.')
        overlapping_bookings = Booking.objects.filter(
            listing=self.listing,
            start_date__lt=self.end_date,
            end_date__gt=self.start_date
        ).exclude(pk=self.pk)
        if overlapping_bookings.exists():
            raise ValidationError('Этот листинг уже забронирован на выбранные даты.')
        if self.start_date < timezone.now().date():
            raise ValidationError('Нельзя бронировать на прошедшие даты.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
