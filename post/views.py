from rest_framework.viewsets import ModelViewSet

from post.models import Post
from post.permissions import IsPostOwnerOrAdminUserOrReadOnly
from post.serializers import PostSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsPostOwnerOrAdminUserOrReadOnly]
