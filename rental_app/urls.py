from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from listings.views import ReservationViewSet, ReviewViewSet
from accounts import views as accounts_views
from listings import views as listings_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'listings', listings_views.ListingViewSet)
router.register(r'reservations', ReservationViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('accounts/', include('accounts.urls')),
    path('api/register/', accounts_views.RegisterView.as_view(), name='register'),
    path('api/login/', accounts_views.LoginView.as_view(), name='login'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
