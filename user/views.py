from rest_framework.generics import ListAPIView

from user.models import User
from user.serializers import UserSerializer


class UserAPI(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
