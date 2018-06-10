from django.core.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField, SerializerMethodField, CharField, EmailField
from account.models import Profile
from posts.models import Post
from account.utils import check_mail_validity_with_email_hippo, get_person_detail_based_on_provided_email
from urllib import request as request_lib
from django.core.files.base import ContentFile
from django.utils.text import slugify
from django.contrib.auth.models import User


post_url = HyperlinkedIdentityField(
        view_name='api:post-detail-view',
        lookup_field='pk',
    )
post_delete_url = HyperlinkedIdentityField(
        view_name='api:post-delete-view',
        lookup_field='pk',
    )

user_url = HyperlinkedIdentityField(
    view_name='api:user-detail-view',
    lookup_field='pk',
)

profile_url = HyperlinkedIdentityField(
    view_name='api:profile-detail-view',
    lookup_field='pk',
)


class ProfileSerializer(ModelSerializer):
    url = profile_url
    user = SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('id', 'url', 'user', 'date_of_birth', 'photo')
        extra_kwargs = {
            'user': {'read_only': True},
        }

    def get_user(self, obj):
        return obj.user.username


class UserCreateSerializer(ModelSerializer):
    profile = ProfileSerializer(required=True)
    url = user_url
    email = EmailField(label='Email address')

    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'first_name', 'last_name', 'email', 'password', 'posts_liked', 'blog_posts', 'is_active', 'profile')
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True},
            'url': {'read_only': True},
            'posts_liked': {'read_only': True},
            'blog_posts': {'read_only': True},
            'is_active': {'read_only': True},
            'profile': {'read_only': True}

        }

    def validate_email(self, value):
        user_queryset = User.objects.filter(email=value)
        if user_queryset.exists():
            raise ValidationError('This email address is already in use')
        return value

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
        )

        user.set_password(validated_data['password'])
        # user.posts_liked.set(validated_data['posts_liked'])
        # user.blog_posts.set(validated_data['blog_posts'])
        # user_data = get_person_detail_based_on_provided_email(user.email)
        # if not user.first_name:
        #     try:
        #         user.first_name = user_data['name']['givenName']
        #     except TypeError:
        #         pass
        # if not user.last_name:
        #     try:
        #         user.last_name = user_data['name']['familyName']
        #     except TypeError:
        #         pass
        user.save()
        # try:
        #     photo_url = user_data['avatar']
        #     response = request_lib.urlopen(photo_url)
        #     image_name = '{}.jpg'.format(slugify(user.username))
        #     user.profile.photo.save(image_name, ContentFile(response.read()))
        # except TypeError:
        #     pass

        return user


    # def validate_email(self, value):
    #     response = check_mail_validity_with_email_hippo(value)
    #     if response != 'Ok':
    #         raise serializers.ValidationError("Please enter a valid email address")
    #         # pass
    #     return value


class PostSerializer(ModelSerializer):
    url = post_url
    delete_url = post_delete_url
    author = UserCreateSerializer(required=True)

    class Meta:
        model = Post
        fields = ('id', 'url', 'delete_url', 'title', 'body', 'users_like', 'status', 'author'  )

    # def update(self, instance, validated_data):
    #     super().update(instance, validated_data)
    #     instance.users_like.remove(instance.author)
    #     instance.save()
    #     return instance


class PostCreateUpdateSerializer(ModelSerializer):
    url = post_url
    delete_url = post_delete_url

    class Meta:
        model = Post
        fields = ('title', 'url', 'delete_url', 'body', 'status')


# class UserLoginSerializer(ModelSerializer):
#     token = CharField(allow_blank=True, read_only=True)
#     username = CharField(required=False, allow_blank=True)
#
#     class Meta:
#         model = User
#         fields = ('username', 'password', 'token')
#         extra_kwargs = {
#             'token': {'read_only': True},
#         }
#
#     def validate(self, data):
#         user_object = None
#         username = data.get('username', None)
#         password = data.get('password')
#         if not username:
#             raise ValidationError('You must provide username to login.')
#         user = User.objects.filter(username=username)
#         if user.exists() and user.count() == 1:
#             user_object = user.first()
#         else:
#             raise ValidationError('User with the given username doesn\'t exist.')
#         if user_object:
#             if not user_object.check_password(password):
#                 raise ValidationError('Wrong password. Please try again.')
#         data['token'] = 'RANDOM_TOKEN'
#         return data
