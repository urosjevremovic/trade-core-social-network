from django.shortcuts import get_object_or_404, redirect
from rest_framework import viewsets
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, DestroyAPIView, CreateAPIView, GenericAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from posts.models import Post
from account.models import Profile
from django.contrib.auth.models import User
from .serializers import PostSerializer, UserCreateSerializer, ProfileSerializer, PostCreateUpdateSerializer
# from .serializers import UserLoginSerializer
from .permissions import IsPostOwnerOrReadOnly, IsAccountOwnerOrReadOnly, IsAnonymousUser
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.decorators import detail_route

class PostListView(ListAPIView):
    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = 'posts/list.html'
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny, ]

    # def get(self, request):
    #     queryset = Post.objects.all()
    #     pagination_class = PostPageNumberPagination
    #     return Response({'posts': queryset, 'page': pagination_class})


class MyPostsListView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


class PostRetrieveView(RetrieveAPIView):
    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = 'posts/detail.html'
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # permission_classes = [AllowAny, ]

    # def get(self, request, pk):
    #     post = get_object_or_404(Post, pk=pk)
    #     serializer = PostSerializer(post)
    #     return Response({'serializer': serializer, 'post': post})


class PostUpdateView(RetrieveUpdateAPIView):
    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = 'posts/detail.html'
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsPostOwnerOrReadOnly]

    # def perform_update(self, serializer):
    #     serializer.save(author=self.request.user)


# class PostLikeView(RetrieveUpdateAPIView):
#     # renderer_classes = [TemplateHTMLRenderer]
#     # template_name = 'posts/detail.html'
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]
#
#     def perform_update(self, serializer):
#         serializer.save()
#
#     @detail_route(methods=['post'],
#                   permission_classes=[IsAuthenticated])
#     def like(self, request, pk, format=None):
#         post = get_object_or_404(Post, pk=pk)
#         post.users_like.add(request.user)
#         return Response({'liked': True})

    # def get(self, request, pk):
    #     post = get_object_or_404(Post, pk=pk)
    #     serializer = PostSerializer(post)
    #     return Response({'serializer': serializer, 'post': post})
    #
    # def post(self, request, pk):
    #     post = get_object_or_404(Post, pk=pk)
    #     serializer = ProfileSerializer(post, data=request.data)
    #     if not serializer.is_valid():
    #         return Response({'serializer': serializer, 'post': post})
    #     serializer.save()
    #     return redirect('api:post-view')


class PostDestroyView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsPostOwnerOrReadOnly]

    def get(self, request, pk, format=None):
        post = get_object_or_404(Post, pk=pk)
        if post.author == request.user:
            post.delete()
            return Response({'deleted': True})
        return Response({'deleted': 'You can not delete other people posts.'})

    # def perform_destroy(self, instance):
    #     if instance.author == self.request.user or self.request.user.is_staff is True:
    #         instance.delete()


class PostCreateView(CreateAPIView):
    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = 'posts/create.html'
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # def get(self, request, pk):
    #     post = get_object_or_404(Post, pk=pk)
    #     serializer = PostSerializer(post)
    #     return Response({'serializer': serializer, 'post': post})

    # def post(self, request, pk):
    #     post = get_object_or_404(Post, pk=pk)
    #     serializer = PostSerializer(post, data=request.data)
    #     if not serializer.is_valid():
    #         return Response({'serializer': serializer, 'post': post})
    #     serializer.save()
    #     return redirect('api:post-view')


# class PostLikeView(GenericAPIView):
#     permission_classes = [IsAuthenticated, ]
#     serializer_class = PostSerializer
#
#     def get(self, request, pk, format=None):
#         post = get_object_or_404(Post, pk=pk)
#         if post.author != request.user:
#             if request.user not in post.users_like.all():
#                 post.users_like.add(request.user)
#                 return Response({'liked': True})
#             else:
#                 post.users_like.remove(request.user)
#                 return Response({'unliked': True})
#         return Response({'liked': 'You can not like your own posts.'})


class PostLikeView(RetrieveAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, ]

    def get(self, request, pk, format=None):
        post = get_object_or_404(Post, pk=pk)
        if post.author != request.user:
            if request.user not in post.users_like.all():
                post.users_like.add(request.user)
                return Response({'liked': True})
            else:
                pass
        else:
            return Response({'liked': 'You can not like your own posts.'})
        return Response({})


# class PostUpdateView(RetrieveUpdateAPIView):
#     # renderer_classes = [TemplateHTMLRenderer]
#     # template_name = 'posts/detail.html'
#     queryset = Post.objects.all()
#     serializer_class = PostCreateUpdateSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
#
#     def perform_update(self, serializer):
#         serializer.save(author=self.request.user)

class ProfileView(ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileRetrieveView(RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    # permission_classes = [AllowAny, ]


class UserView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class UserRetrieveView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    # permission_classes = [AllowAny, ]


class UserUpdateView(RetrieveUpdateDestroyAPIView):
    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = 'posts/detail.html'
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAccountOwnerOrReadOnly]

    # def perform_update(self, serializer):
    #     serializer.save(user=self.request.user)


class UserCreateView(CreateAPIView):
    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = 'posts/create.html'
    # queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [IsAnonymousUser, ]


# class UserLoginView(GenericAPIView):
#     # renderer_classes = [TemplateHTMLRenderer]
#     # template_name = 'posts/create.html'
#     # queryset = User.objects.all()
#     serializer_class = UserLoginSerializer
#     permission_classes = [AllowAny, ]
#
#     def post(self, request, *args, **kwargs):
#         data = request.data
#         serializer = UserLoginSerializer(data=data)
#         if serializer.is_valid(raise_exception=True):
#             new_data = serializer.data
#             return Response(new_data, status=HTTP_200_OK)
#         return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
