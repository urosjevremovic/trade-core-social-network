from django.utils import timezone
from rest_framework import serializers
from account.models import Profile
from posts.models import Post
from django.contrib.auth.models import User
from account.utils import check_mail_validity_with_email_hippo, get_person_detail_based_on_provided_email
from urllib import request as request_lib
from django.core.files.base import ContentFile
from django.utils.text import slugify

from posts.utils import code_generator


class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'url', 'title', 'author', 'body', 'users_like', 'status')

    def create(self, validated_data):
        list_of_post_names = []
        posts = Post.objects.all()
        for post in posts:
            if post.publish.day == timezone.now().day and post.publish.month == timezone.now().month and \
                    post.publish.year == timezone.now().year:
                list_of_post_names.append(post.title)
        post = Post.objects.create(
            title=validated_data['title'],
            author=validated_data['author'],
            body=validated_data['body'],
            status=validated_data['status'],
        )

        post.users_like.set(validated_data['users_like'])
        if post.title in list_of_post_names:
            post.title = post.title + code_generator()

        return post


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'user', 'date_of_birth', 'photo')
        extra_kwargs = {
            'user': {'read_only': True},
        }


class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = ProfileSerializer(required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password', 'profile')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user_data = get_person_detail_based_on_provided_email(user.email)
        if not user.first_name:
            try:
                user.first_name = user_data['name']['givenName']
            except TypeError:
                pass
        if not user.last_name:
            try:
                user.last_name = user_data['name']['familyName']
            except TypeError:
                pass
        user.save()
        profile = Profile.objects.create(user=user)
        photo_url = user_data['avatar']
        response = request_lib.urlopen(photo_url)
        image_name = '{}.jpg'.format(slugify(user.username))
        user.profile.photo.save(image_name, ContentFile(response.read()))

        return user

    def validate_email(self, value):
        response = check_mail_validity_with_email_hippo(value)
        if response != 'Ok':
            raise serializers.ValidationError("Please enter a valid email address")
        return value
