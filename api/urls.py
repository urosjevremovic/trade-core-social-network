from django.urls import path, include
from .views import PostListView, UserView, ProfileView, PostRetrieveView, PostDestroyView, \
    PostUpdateView, PostCreateView, MyPostsListView, UserRetrieveView, ProfileRetrieveView, \
    PostLikeView, UserUpdateView, UserCreateView
# from .views import UserLoginView
from rest_framework import routers

# router = routers.DefaultRouter()
# router.register('posts', PostView)
# router.register('users', UserView)
# router.register('profiles', ProfileView)
#
#
# urlpatterns = [
#     path('', include(router.urls)),
# ]

app_name = 'api'
urlpatterns = [
    path('post_view/', PostListView.as_view(), name='post-view'),
    path('my_posts_view/', MyPostsListView.as_view(), name='my-posts-view'),
    path('user_view/', UserView.as_view(), name='user-update-view'),
    path('user_view/register/', UserCreateView.as_view(), name='user-create-view'),
    path('user_view/<int:pk>/edit/', UserUpdateView.as_view(), name='user-view'),
    path('user_view/<int:pk>/', UserRetrieveView.as_view(), name='user-detail-view'),
    path('profile_view/', ProfileView.as_view(), name='profile-view'),
    path('profile_view/<int:pk>/', ProfileRetrieveView.as_view(), name='profile-detail-view'),
    path('post_view/<int:pk>/', PostRetrieveView.as_view(), name='post-detail-view'),
    path('post_view/<int:pk>/edit/', PostUpdateView.as_view(), name='post-edit-view'),
    path('post_view/<int:pk>/delete/', PostDestroyView.as_view(), name='post-delete-view'),
    path('post_view/<int:pk>/like/', PostLikeView.as_view(), name='post-like-view'),
    path('post_view/create/', PostCreateView.as_view(), name='post-create-view'),
]
