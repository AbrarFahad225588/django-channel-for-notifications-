from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/", include("posts.urls")),
    path("api/notifications/", include("notifications.urls")),
]

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from .views import LoginView, LogoutView,RegisterView,UsersView,UserDetailView

urlpatterns+= [

    path("api/login/", LoginView.as_view()),
    path("api/logout/", LogoutView.as_view()),
    path("api/refresh/", TokenRefreshView.as_view()),
    path("api/register/",RegisterView.as_view()),
    path("api/users/",UsersView.as_view()),
    path("api/users/<int:pk>/",UserDetailView.as_view()),


]