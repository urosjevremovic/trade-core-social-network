from django.urls import path, include
from .views import PostView, UserView, ProfileView
from rest_framework import routers

router = routers.DefaultRouter()
router.register('posts', PostView)
router.register('users', UserView)
router.register('profiles', ProfileView)


urlpatterns = [
    path('', include(router.urls)),
]
