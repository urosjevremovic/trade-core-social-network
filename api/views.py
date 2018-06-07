from rest_framework import viewsets
from posts.models import Post
from account.models import Profile
from django.contrib.auth.models import User
from .serializers import PostSerializer, UserSerializer, ProfileSerializer


class PostView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class ProfileView(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

