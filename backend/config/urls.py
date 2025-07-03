from django.contrib import admin
from django.urls import path, include, re_path

# Import the token-related views provided by the simplejwt library.
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    re_path(r"^healthz/ready/?$", views.Healthcheck.as_view()),
    path("api/v1/rooms/", include("rooms.urls")),
    path("api/v1/categories/", include("categories.urls")),
    path("api/v1/experiences/", include("experiences.urls")),
    path("api/v1/medias/", include("medias.urls")),
    path("api/v1/wishlists/", include("wishlists.urls")),
    # --- JWT Authentication Endpoints ---
    # 1. Endpoint to obtain a new token pair (access and refresh tokens).
    #    Clients send a POST request with 'username' and 'password' to this URL.
    # path("api/v1/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # 2. Endpoint to refresh an expired access token.
    #    Clients send a POST request with their 'refresh' token to get a new 'access' token.
    # path("api/v1/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # path("api/v1/auth/login/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/v1/auth/", include("users.urls")),
]
