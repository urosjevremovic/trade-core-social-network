from django.urls import path

from post.views import PostViewSet


app_name = 'posts'
urlpatterns = [
    path('', PostViewSet.as_view(), name='posts'),
]