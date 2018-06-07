from rest_framework import serializers
from account.models import Profile
from posts.models import Post
from django.contrib.auth.models import User
from account.utils import check_mail_validity_with_email_hippo, get_person_detail_based_on_provided_email
from urllib import request as request_lib


class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'url', 'title', 'author', 'body', 'users_like', 'status')


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'user', 'date_of_birth', 'photo')
        extra_kwargs = {
            'user': {'read_only': True},
        }
    # try:
    #     user_data = get_person_detail_based_on_provided_email(mail)
    #     photo_url = user_data['avatar']
    #     response = request_lib.urlopen(photo_url)
    #     photo = serializers.ImageField
    #     image_name = '{}.jpg'.format(slugify(new_user.username))
    #     photo.save(image_name, ContentFile(response.read()))


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

        profile = Profile.objects.create(user=user)

        return user

    def validate_email(self, value):
        response = check_mail_validity_with_email_hippo(value)
        if response != 'Ok':
            raise serializers.ValidationError("Please enter a valid email address")
        return value
