from django.shortcuts import get_object_or_404
from rest_framework import mixins
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.reverse import reverse
from rest_framework.response import Response

from posts.models import Post
from account.models import Profile
from django.contrib.auth.models import User
from .serializers import PostSerializer, UserCreateSerializer, ProfileSerializer, PostCreateUpdateSerializer
from .permissions import IsPostOwnerOrAdminUserOrReadOnly, IsAnonymousUser, IsAccountwnerOrAdminUserOrReadOnly


@api_view(['GET'])
def api_home(request):
    data = {
        'posts': {
            'count': Post.objects.count(),
            'url': reverse('api:post-list-view'),
        },
        'users': {
            'count': User.objects.count(),
            'url': reverse('api:user-list-view'),
        },
        'profiles': {
            'count': Profile.objects.count(),
            'url': reverse('api:profile-list-view'),
        },
    }
    return Response(data)


class PostListView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny, ]


class MyPostsListView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


class PostRetrieveView(mixins.DestroyModelMixin, mixins.UpdateModelMixin, RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsPostOwnerOrAdminUserOrReadOnly]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class PostCreateView(CreateAPIView):
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostLikeView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsAuthenticated, ]

    def get(self, request, pk, format=None):
        post = get_object_or_404(Post, pk=pk)
        if post.author != request.user:
            if request.user not in post.users_like.all():
                post.users_like.add(request.user)
                return Response({'liked': 'Liked'})
            else:
                return Response({'liked': 'You already liked this posts.'})
        else:
            return Response({'liked': 'You can not like your own posts.'})


class PostUnlikeView(RetrieveAPIView):
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsAuthenticated, ]

    def get(self, request, pk, format=None):
        post = get_object_or_404(Post, pk=pk)
        if request.user in post.users_like.all():
            post.users_like.remove(request.user)
            return Response({'unliked': 'Unliked'})
        else:
            return Response({'unliked': 'Post is not not liked, so you can\'t unlike it.'})


class ProfileListView(ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileRetrieveView(RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class UserRetrieveView(mixins.DestroyModelMixin, RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [IsAccountwnerOrAdminUserOrReadOnly, ]

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class UserCreateView(CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = [IsAnonymousUser, ]

