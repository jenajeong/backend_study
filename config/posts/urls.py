from django.urls import path
from .views import PostList, PostCreateView, PostRetrieveUpdateDestroyView

urlpatterns = [
    path('',PostList.as_view(), name='post-list'),
    path('create/', PostCreateView.as_view(), name='post-create'),
    path('<int:pk>',PostRetrieveUpdateDestroyView.as_view(), name='post-detail'),
]
