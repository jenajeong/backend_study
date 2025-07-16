from django.urls import path
from .views import PostListView, PostCreateView, PostRetrieveUpdateDestroyView,toggle_like

urlpatterns = [
    path('',PostListView.as_view(), name='post-list'),
    path('create/', PostCreateView.as_view(), name='post-create'),
    path('<int:pk>',PostRetrieveUpdateDestroyView.as_view(), name='post-detail'),
    path('post/<int:post_id>/like/', toggle_like, name='toggle_like'),
]
