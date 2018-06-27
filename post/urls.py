from django.urls import path

from post.views import PostAPI


app_name = 'posts'
urlpatterns = [
    path('', PostAPI.as_view(), name='posts'),
]