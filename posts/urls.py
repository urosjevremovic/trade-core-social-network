from django.urls import path
from .views import post_detail, post_list, post_create, users_post_list, post_like


app_name = 'posts'
urlpatterns = [
    path('', post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>', post_detail, name='post_detail'),
    path('create/', post_create, name='post_create'),
    path('users_posts/', users_post_list, name='users_post_list'),
    path('like/', post_like, name='post_like'),
]
