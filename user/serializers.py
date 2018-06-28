from django.core.files.base import ContentFile
from django.utils.text import slugify
from rest_framework import serializers

from user.models import User
from user.utils import get_person_detail_based_on_provided_email

from urllib import request as request_lib


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
        user_data = get_person_detail_based_on_provided_email(user.email)
        try:
            user.first_name = user_data['person']['name']['givenName']
            user.last_name = user_data['person']['name']['familyName']
        except TypeError:
            pass
        try:
            photo_url = user_data['person']['avatar']
            response = request_lib.urlopen(photo_url)
            image_name = '{}.jpg'.format(slugify(user.username))
            user.photo.save(image_name, ContentFile(response.read()))
        except (TypeError, AttributeError):
            pass
        user.save()
        return user

