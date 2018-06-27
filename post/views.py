from rest_framework.generics import ListAPIView

from post.models import Post
from post.serializers import PostSerializer


class PostAPI(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
