# urls.py
from django.urls import path
from .views import (
    NotificationListView, NotificationDetailView,
    MarkAllAsReadView, UnreadCountView
)

urlpatterns = [
    path('', NotificationListView.as_view(), name='notification-list'),
    path('<int:id>/', NotificationDetailView.as_view(), name='notification-detail'),
    path('mark-all-read/', MarkAllAsReadView.as_view(), name='mark-all-read'),
    path('unread-count/', UnreadCountView.as_view(), name='unread-count'),
]