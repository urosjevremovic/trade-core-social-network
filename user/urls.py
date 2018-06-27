from django.urls import path

from user.views import UserViewSet

app_name = 'users'
urlpatterns = [
    path('', UserViewSet.as_view(), name='users'),
]