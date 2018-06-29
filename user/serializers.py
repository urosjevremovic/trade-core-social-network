from rest_framework import serializers

from user.tasks import additiona_info_about_user
from user.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'is_active', 'date_joined',
                  'posts_liked', 'blog_posts', 'date_of_birth', 'photo')
        extra_kwargs = {
            'is_active': {'read_only': True},
            'date_joined': {'read_only': True},
            'password': {'write_only': True},
            'posts_liked': {'read_only': True},
            'blog_posts': {'read_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
        )

        user.set_password(validated_data['password'])
        user.save()
        additiona_info_about_user.delay(user.id)
        return user

