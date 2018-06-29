from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from post.models import Post
from post.permissions import IsPostOwnerOrAdminUserOrReadOnly
from post.serializers import PostSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated, ]
        elif self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            permission_classes = [IsPostOwnerOrAdminUserOrReadOnly, ]
        else:
            permission_classes = [AllowAny, ]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(methods=['get'], detail=True)
    def like(self, request, pk=None):
        post = self.get_object()
        if request.user == post.author:
            return Response({'status': 'You can not like your own posts'}, status=403)
        if request.user in post.users_like.all():
            post.users_like.remove(request.user)
            post.save()
            return Response({'status': 'unliked'})
        else:
            post.users_like.add(request.user)
            post.save()
            return Response({'status': 'liked'})
