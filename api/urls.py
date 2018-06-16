from django.urls import path
from .views import (PostListView, UserListView, ProfileListView, PostRetrieveView, PostCreateView,
                    MyPostsListView, UserRetrieveView, ProfileRetrieveView, UserCreateView,
                    PostLikeView, PostUnlikeView)

app_name = 'api'
urlpatterns = [
    path('register/', UserCreateView.as_view(), name='user-create-view'),
    path('user-list/', UserListView.as_view(), name='user-list-view'),
    path('user-list/<int:pk>/', UserRetrieveView.as_view(), name='user-detail-view'),
    path('profile-list/', ProfileListView.as_view(), name='profile-list-view'),
    path('profile-list/<int:pk>/', ProfileRetrieveView.as_view(), name='profile-detail-view'),
    path('post-list/create/', PostCreateView.as_view(), name='post-create-view'),
    path('my-posts-list/', MyPostsListView.as_view(), name='my-posts-list-view'),
    path('post-list/', PostListView.as_view(), name='post-list-view'),
    path('post-list/<int:pk>/', PostRetrieveView.as_view(), name='post-detail-view'),
    path('post-list/<int:pk>/like/', PostLikeView.as_view(), name='post-like-view'),
    path('post-list/<int:pk>/unlike/', PostUnlikeView.as_view(), name='post-unlike-view'),
]
