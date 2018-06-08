from django.utils import timezone
from rest_framework import serializers
from account.models import Profile
from posts.models import Post
from django.contrib.auth.models import User
from account.utils import check_mail_validity_with_email_hippo, get_person_detail_based_on_provided_email
from urllib import request as request_lib
from django.core.files.base import ContentFile
from django.utils.text import slugify
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User


class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'url', 'title', 'author', 'body', 'users_like', 'status')

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        if instance.users_like == instance.author:
            instance.users_like.remove(instance.author)
            instance.save()
        return instance


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
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password', 'profile', 'posts_liked', 'blog_posts')
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

        @receiver(post_save, sender=User)
        def create_or_update_user_profile(sender, instance, created, **kwargs):
            if created:
                Profile.objects.create(user=instance)
            instance.profile.save()

        user.set_password(validated_data['password'])
        user.posts_liked.set(validated_data['posts_liked'])
        user.blog_posts.set(validated_data['blog_posts'])
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
        try:
            photo_url = user_data['avatar']
            response = request_lib.urlopen(photo_url)
            image_name = '{}.jpg'.format(slugify(user.username))
            user.profile.photo.save(image_name, ContentFile(response.read()))
        except TypeError:
            pass

        return user

    #
    # def validate_email(self, value):
    #     response = check_mail_validity_with_email_hippo(value)
    #     if response != 'Ok':
    #         raise serializers.ValidationError("Please enter a valid email address")
    #         # pass
    #     return value

