"""trade_core_social_network URL Configuration

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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import (password_change, password_change_done, password_reset, password_reset_complete,
                                       password_reset_confirm, password_reset_done)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from account.views import dashboard

from api.views import api_home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls'), name='account'),
    path('', dashboard, name='dashboard'),
    path('posts/', include('posts.urls'), name='posts'),
    path('api/', api_home, name='api'),
    path('api/', include('api.urls'), name='api'),
    path('api-auth/', include('rest_framework.urls'), name='api-auth'),
    path('api/token/', TokenObtainPairView.as_view(), name='api-token'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='api-token-refresh'),
    path('password_change/', password_change, name='password_change'),
    path('password_change/done/', password_change_done, name='password_change_done'),
    path('password_reset/', password_reset, name='password_reset'),
    path('password_reset_complete/', password_reset_complete, name='password_reset_complete'),
    path('password_reset_confirm/<str:uidb64>/<str:token>/', password_reset_confirm, name='password_reset_confirm'),
    path('password_reset_done/', password_reset_done, name='password_reset_done'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
