from rest_framework import serializers
from .models import Post
from django.contrib.auth.models import User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
class PostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    likes = UserSerializer(many=True, read_only=True)
    is_liked = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'likes', 'author','like_count','is_liked', 'created_at', 'updated_at']
    def get_author(self, obj):
        return obj.author.username  
    def get_like_count(self, obj):
        return len(obj.likes.all())  
    def get_is_liked(self, obj):
        user = self.context['request'].user
        return user in obj.likes.all()