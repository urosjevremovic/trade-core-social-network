from django.urls import path

from user.views import UserAPI


app_name = 'users'
urlpatterns = [
    path('', UserAPI.as_view(), name='users'),
]