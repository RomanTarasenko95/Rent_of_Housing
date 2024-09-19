from rest_framework import viewsets, filters, status
from .models import Listing, Review, Booking
from .permissions import IsOwnerOrReadOnly
from .serializers import ListingSerializer, ReviewSerializer, BookingSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.core.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from listings.forms import RegisterForm, LoginForm
from django.http import HttpResponse
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.urls import reverse_lazy
from rest_framework.response import Response
from rest_framework.decorators import action


class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()  # Выборка всех объявлений
    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,]

    # Фильтрация, поиск и сортировка
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Поля для фильтрации
    filterset_fields = ['price', 'location', 'number_of_rooms', 'property_type']

    # Поля для поиска по заголовку и описанию
    search_fields = ['title', 'description']

    # Поля для сортировки (по цене и дате добавления)
    ordering_fields = ['price', 'created_at']

    def perform_create(self, serializer):
        # Проверка, что пользователь в группе 'Арендодатель'
        if self.request.user.role != 'landlord':
            raise PermissionDenied("Только арендодатели могут создавать объявления.")
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        # Проверка, чтобы только владелец мог редактировать объявление
        if serializer.instance.owner != self.request.user:
            raise PermissionDenied("Вы не можете редактировать это объявление.")
        serializer.save()

    def perform_destroy(self, instance):
        # Проверка, чтобы только владелец мог удалять объявление
        if instance.owner != self.request.user:
            raise PermissionDenied("Вы не можете удалить это объявление.")
        instance.delete()


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Устанавливаем пользователя при создании отзыва
        serializer.save(user=self.request.user)


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    def perform_create(self, serializer):
        # Устанавливаем арендатора при создании бронирования
        serializer.save(renter=self.request.user)

    def perform_update(self, serializer):
        # Если пользователь пытается подтвердить бронирование
        if 'is_confirmed' in self.request.data and not self.request.user == serializer.instance.listing.owner:
            raise PermissionDenied("Вы не можете подтвердить бронирование, так как не являетесь владельцем листинга.")
        super().perform_update(serializer)


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Перенаправление на главную страницу
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Перенаправление на главную страницу
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def home(request):
    if request.method == 'POST' and 'logout' in request.POST:
        logout(request)
        return redirect('login')  # Перенаправление на страницу входа после выхода

    context = {
        'api_listings_url': '/api/listings/',
        'api_reviews_url': '/api/reviews/',
        'api_bookings_url': '/api/bookings/',
        'register_url': '/register/',
        'login_url': '/login/',
        'is_authenticated': request.user.is_authenticated,
    }
    return render(request, 'home.html', context)


class CustomLogoutView(DjangoLogoutView):
    next_page = reverse_lazy('login')
