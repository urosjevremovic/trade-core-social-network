"""social_network_REST_API URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token

from post.views import PostViewSet
from user.views import UserViewSet

router = DefaultRouter()
router.register('posts', PostViewSet)
router.register('users', UserViewSet)


urlpatterns = [
    path('obtain-token/', obtain_jwt_token),
    path(r'login/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += router.urls
