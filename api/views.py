from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, DestroyAPIView, CreateAPIView, GenericAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from posts.models import Post
from account.models import Profile
from django.contrib.auth.models import User
from .serializers import PostSerializer, UserCreateSerializer, ProfileSerializer, PostCreateUpdateSerializer
from .permissions import IsPostOwnerOrAdminUserOrReadOnly, IsAnonymousUser
from rest_framework.response import Response


class PostListView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny, ]


class MyPostsListView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


class PostRetrieveView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostUpdateView(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsPostOwnerOrAdminUserOrReadOnly]


class PostDestroyView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        post = get_object_or_404(Post, pk=pk)
        if post.author == request.user or request.user.is_staff:
            post.delete()
            return Response({'deleted': True})
        return Response({'deleted': 'You can not delete other people posts.'})


class PostCreateView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostLikeView(RetrieveAPIView):
    serializer_class = PostSerializer
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
    serializer_class = PostSerializer
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


class UserRetrieveView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class UserCreateView(CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = [IsAnonymousUser, ]


class UserDestroyView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        user = get_object_or_404(User, pk=pk)
        if user == request.user or request.user.is_staff:
            user.delete()
            return Response({'deleted': True})
        return Response({'deleted': 'You can not delete other people accounts.'})

