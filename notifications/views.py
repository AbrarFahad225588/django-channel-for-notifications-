# views.py (or using ViewSets)
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer, UnreadCountSerializer
from .services import mark_notification_as_read, mark_all_as_read, get_unread_count
from .selectors import get_notifications
from .permissions import IsRecipientOrReadOnly
from rest_framework.pagination import CursorPagination


class NotificationCursorPagination(CursorPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100

    # Newest notification first
    ordering = "-created_at"
from rest_framework import generics, permissions

from .models import Notification
from .serializers import NotificationSerializer
from .selectors import get_notifications


class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = NotificationCursorPagination

    def get_queryset(self):
        return get_notifications(
            self.request.user,
            filters=self.request.query_params,
        )

class NotificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated, IsRecipientOrReadOnly]
    lookup_field = 'id'
    
    def perform_update(self, serializer):
        # mark as read via service
        notification = self.get_object()
        mark_notification_as_read(notification.id, self.request.user)
        serializer.instance.refresh_from_db()
    
    def perform_destroy(self, instance):
        # Soft delete if enabled, else hard delete
        if hasattr(instance, 'is_deleted'):
            instance.is_deleted = True
            instance.save(update_fields=['is_deleted'])
        else:
            instance.delete()

class MarkAllAsReadView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        count = mark_all_as_read(request.user)
        return Response({'marked_count': count})

class UnreadCountView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        count = get_unread_count(request.user)
        return Response(UnreadCountSerializer({'count': count}).data)