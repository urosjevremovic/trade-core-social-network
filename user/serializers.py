from rest_framework import serializers

from user.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'is_active', 'date_joined', 'date_of_birth', 'photo')
        extra_kwargs = {
            'is_active': {'read_only': True},
            'date_joined': {'read_only': True},
        }

