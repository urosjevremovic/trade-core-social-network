from django.core.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField, SerializerMethodField, EmailField
from account.models import Profile
from posts.models import Post
from account.utils import check_mail_validity_with_email_hippo, get_person_detail_based_on_provided_email, check_mail_validity_with_never_bounce, check_mail_validity_with_email_hunter
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
    url = user_url
    email = EmailField(label='Email address')

    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'first_name', 'last_name', 'email', 'password', 'posts_liked', 'blog_posts', 'is_active',)
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
        response = check_mail_validity_with_never_bounce(value)
        if response != 'disposable' and response != 'valid':
            print(response)
            raise ValidationError("fuck enter a valid email address")
        if user_queryset.exists():
            raise ValidationError('This email address is already in use')
        return value

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
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
        try:
            photo_url = user_data['avatar']
            response = request_lib.urlopen(photo_url)
            image_name = '{}.jpg'.format(slugify(user.username))
            user.profile.photo.save(image_name, ContentFile(response.read()))
        except (TypeError, AttributeError):
            pass

        return user


class PostSerializer(ModelSerializer):
    url = post_url
    delete_url = post_delete_url
    author = UserCreateSerializer(required=True)

    class Meta:
        model = Post
        fields = ('id', 'url', 'delete_url', 'title', 'body', 'users_like', 'status', 'author'  )


class PostCreateUpdateSerializer(ModelSerializer):
    url = post_url
    delete_url = post_delete_url

    class Meta:
        model = Post
        fields = ('title', 'url', 'delete_url', 'body', 'status')

