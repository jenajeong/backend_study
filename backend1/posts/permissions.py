from rest_framework import permissions
from rest_framework.permissions import BasePermission
    
class IsOwnerOrReadOnly(BasePermission):  # BasePermission만 상속, 작성자 이외엔 읽기만 가능
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:  # GET, HEAD, OPTIONS 허용
            return True
        return obj.author == request.user  # 이외는 작성자만 가능