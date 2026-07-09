# views.py (or using ViewSets)
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer, UnreadCountSerializer
from .services import mark_notification_as_read, mark_all_as_read, get_unread_count
from .selectors import get_notifications
from .permissions import IsRecipientOrReadOnly

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.for_recipient(self.request.user)
    
    def list(self, request, *args, **kwargs):
        # Use selector for performance and ordering
        queryset, count = get_notifications(
            request.user,
            filters=request.query_params.dict(),
            page=int(request.query_params.get('page', 1)),
            page_size=int(request.query_params.get('page_size', 20))
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'results': serializer.data,
            'count': count,
        })

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