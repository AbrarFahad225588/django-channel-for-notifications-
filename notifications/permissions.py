# permissions.py
from rest_framework.permissions import BasePermission
from rest_framework import permissions

class IsRecipientOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow safe methods for anyone (but list filtered by recipient)
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.recipient == request.user