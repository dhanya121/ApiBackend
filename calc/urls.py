from django.urls import path
from .views import RegisterView, CalculationViewSet, LogoutView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterView.as_view(), name="sign_up"),
    path('calculations/', CalculationViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('calculations/<int:pk>/', CalculationViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('api/logout/', LogoutView.as_view(), name='logout'),


]