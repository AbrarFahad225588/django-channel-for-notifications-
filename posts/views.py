from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Post
from .serializers import PostSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from notifications.services import send_notification
from rest_framework.generics import GenericAPIView,ListCreateAPIView,RetrieveAPIView
from rest_framework.authentication import authenticate
from django.contrib.auth.models import User
class UserFindView(RetrieveAPIView):
    def get(self, request, *args, **kwargs):
         user = User.objects.get(username=request.user.username)
         print(user.email)
         return Response(data="Hi",status=200,content_type='json')
    

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]
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
            send_notification(
                recipient=post.author,
                actor=user,
                title='New like',
                message=f"{user.username} unliked your post!",
                # celery_async=False
            )
            return Response({'status': 'post unliked'})
        else:
            post.likes.add(user)
            send_notification(
                recipient=post.author,
                actor=user,
                title='New like',
                message=f"{user.username} unliked your post!",
                # celery_async=False
            )
            return Response({'status': 'post liked'})