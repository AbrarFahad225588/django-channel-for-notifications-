from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Post
from .serializers import PostSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from notifications.services import send_notification
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get_queryset(self):
        queryset = super().get_queryset()
        author_id = self.request.query_params.get('author_id')

        if author_id:
            queryset = queryset.filter(author__id=author_id)
        return queryset
    @action(detail=True, methods=['get'], url_path='like')
    def like_post(self, request, pk=None):
        post = self.get_object()
        user = request.user

        if user in post.likes.all():
            post.likes.remove(user)
            return Response({'status': 'post unliked'})
        else:
            post.likes.add(user)
            send_notification(post.author, f"{user.username} liked your post!")
            return Response({'status': 'post liked'})