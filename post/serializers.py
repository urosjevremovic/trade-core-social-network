from rest_framework import serializers

from post.models import Post


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'
        extra_kwargs = {
            'author': {'read_only': True},
            'publish': {'read_only': True},
            'users_like': {'read_only': True},
        }