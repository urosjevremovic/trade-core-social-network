from django.urls import path
from django.contrib.auth.views import (login, logout, logout_then_login, )

from .views import register, edit, user_detail, user_list, activate_user_view

app_name = 'account'
urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('logout_then_login/', logout_then_login, name='logout_then_login'),
    path('register/', register, name='register'),
    path('activate/<code>/', activate_user_view, name='activate'),
    path('edit/', edit, name='edit'),
    path('users/', user_list, name='users_list'),
    path('users/<str:username>/', user_detail, name='users_detail'),
]
