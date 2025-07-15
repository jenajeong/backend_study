from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Post
from .serializers import PostSerializer
# Create your views here.

class PostListView(generics.ListAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny] #목록조회는 누구나
    
class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated] # 새 글 작성은 로그인 된 사람만
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        
class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    selializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] #글 상세 조회, 수정, 삭제 - 로그인 시 가능
    
    
    