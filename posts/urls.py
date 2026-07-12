from django.urls import include, include, path
from .views import PostViewSet,UserFindView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')

urlpatterns = [
    path('', include(router.urls)),
    path('user/',UserFindView.as_view(), name='users'),
]
