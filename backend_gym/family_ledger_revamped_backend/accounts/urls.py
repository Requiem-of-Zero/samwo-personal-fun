from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    RegisterView,
    MeView,
    LogoutView,
    ChangePasswordView,
    UpdateUserView,
    DeactivateUserView
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="auth-register"),
    path("login/", TokenObtainPairView.as_view(), name="auth-login"),
    path("me/", MeView.as_view(), name="auth-me"),
    path("token/refresh", TokenRefreshView.as_view(), name="auth-refresh"),
    path("logout/", LogoutView.as_view(), name="auth-logout"),
    path("change-password/", ChangePasswordView.as_view(), name="auth-change-password"),
    path("update/", UpdateUserView.as_view(), name="auth-update-user"),
    path("deactivate/", DeactivateUserView.as_view(), name="auth-deactivate")
]
