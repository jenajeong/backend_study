from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework import generics, permissions
from .models import Post, Like, Comment
from .permissions import IsOwnerOrReadOnly
from .serializers import PostSerializer, CommentSerializer, ReplySerializer
from django.http import JsonResponse
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
    permission_classes = [IsOwnerOrReadOnly] #글 상세 조회, 수정, 삭제 - 로그인 시 가능

@login_required #로그인 한 유저만
def toggle_like(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        like, created = Like.objects.get_or_create(user=request.user, post=post) #Like모델에서 요청user와 post의 존재 여부에 따라 created 불린값 제공

        if not created:
            like.is_active = not like.is_active # 비활성화
            like.save()
        else:
            like.is_active = True # 활성화
            like.save()

        is_liked = like.is_active
        like_count = post.likes.filter(is_active=True).count() #해당 게시글의 좋아요수 집계

        return JsonResponse({'liked': is_liked, 'like_count': like_count})

class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs['community_id']
        return Comment.objects.filter(post_id=post_id, parent__isnull=True, is_deleted=False)

    def perform_create(self, serializer):
        post_id = self.kwargs['community_id']
        post = get_object_or_404(Post, pk=post_id)
        serializer.save(author=self.request.user, post=post)

class CommentUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

class ReplyCreateView(generics.CreateAPIView):
    serializer_class = ReplySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        parent_id = self.kwargs['comment_id']
        parent = get_object_or_404(Comment, id=parent_id)
        serializer.save(author=self.request.user, post=parent.post, parent=parent)
        
    
    