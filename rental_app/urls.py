from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from listings import views as listings_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny,],
)

router = DefaultRouter()
router.register(r'listings', listings_views.ListingViewSet, basename='api-listings')
router.register(r'reviews', listings_views.ReviewViewSet, basename='api-reviews')
router.register(r'bookings', listings_views.BookingViewSet, basename='api-bookings')

urlpatterns = [
    path('admin/', admin.site.urls),

    # Главная страница и пользовательские страницы
    path('', include('listings.urls')),
    path('api/', include(router.urls)),

    # JWT аутентификация (если используете)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
