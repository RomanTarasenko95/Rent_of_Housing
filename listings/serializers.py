from rest_framework import serializers
from .models import Listing, Review, Booking


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'renter', 'listing', 'start_date', 'end_date', 'is_confirmed']
        read_only_fields = ['renter']

    def get_can_confirm(self, obj):
        request = self.context.get('request')
        # Проверяем, является ли текущий пользователь владельцем листинга
        return request and request.user == obj.listing.owner and not obj.is_confirmed

    def update(self, instance, validated_data):
        request = self.context.get('request')
        # Ограничиваем подтверждение бронирования только для владельцев
        if 'is_confirmed' in validated_data and request.user != instance.listing.owner:
            raise serializers.ValidationError(
                "Вы не можете подтвердить это бронирование, так как вы не являетесь владельцем листинга.")
        return super().update(instance, validated_data)

    def validate(self, data):
        listing = data['listing']
        start_date = data['start_date']
        end_date = data['end_date']

        overlapping_bookings = Booking.objects.filter(
            listing=listing,
            start_date__lt=end_date,
            end_date__gt=start_date
        ).exclude(pk=self.instance.pk if self.instance else None)

        if overlapping_bookings.exists():
            raise serializers.ValidationError("Этот объект уже забронирован на выбранные даты.")
        return data


class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'