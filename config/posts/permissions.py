from rest_framework import permissions
from rest_framework.permissions import BasePermission

class IsOwnerOrReadOnly(permissions,BasePermission): #작성자 이외엔 읽기만 ㄱ가능
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS: # GET, HAED, OPTIONS
            
            return True
        return obj.author == request.user