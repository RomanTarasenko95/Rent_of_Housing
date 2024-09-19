from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ListingViewSet, ReviewViewSet, BookingViewSet
from .views import register, user_login, home, CustomLogoutView

# Создаем маршрутизатор
router = DefaultRouter()
router.register(r'listings', ListingViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    # Основные маршруты для API
    path('api/', include(router.urls)),

    # Маршруты для пользовательских представлений
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),  # Страница выхода

    # Главная страница
    path('', home, name='home'),
]
