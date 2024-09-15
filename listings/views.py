from rest_framework import viewsets
from .models import Listing, Reservation, Review
from .serializers import ListingSerializer, ReservationSerializer, ReviewSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly, IsRenterOrReadOnly


class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [IsOwnerOrReadOnly, IsRenterOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def filter_queryset(self, queryset):
        """
        Фильтруем queryset на основе параметров запроса
        """
        # Получаем параметры из запроса
        price_min = self.request.query_params.get('price_min', None)
        price_max = self.request.query_params.get('price_max', None)
        location = self.request.query_params.get('location', None)
        number_of_rooms = self.request.query_params.get('number_of_rooms', None)
        property_type = self.request.query_params.get('property_type', None)

        # Применяем фильтры к queryset
        if price_min is not None:
            queryset = queryset.filter(price__gte=price_min)
        if price_max is not None:
            queryset = queryset.filter(price__lte=price_max)
        if location is not None:
            queryset = queryset.filter(location__icontains=location)
        if number_of_rooms is not None:
            queryset = queryset.filter(number_of_rooms=number_of_rooms)
        if property_type is not None:
            queryset = queryset.filter(property_type=property_type)

        return queryset

    def get_queryset(self):
        """
        Переопределяем метод get_queryset для использования кастомной фильтрации
        """
        queryset = super().get_queryset()
        return self.filter_queryset(queryset)


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsOwnerOrReadOnly]


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]