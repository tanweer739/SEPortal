from django.urls import path
from . import views
from .views import UserPostListView, PostDeleteView, PostUpdateView, PostCreateView, CommentDeleteView, \
    CommentUpdateView, PostDetailView , PostListView

urlpatterns = [
    path('', PostListView.as_view(), name='activity-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment')
]
