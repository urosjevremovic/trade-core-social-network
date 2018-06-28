from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from user.models import User
from user.permissions import IsAccountwnerOrAdminUserOrReadOnly, IsAnonymousUser
from user.serializers import UserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAccountwnerOrAdminUserOrReadOnly, ]

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAnonymousUser, ]
        elif self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            permission_classes = [IsAccountwnerOrAdminUserOrReadOnly, ]
        else:
            permission_classes = [AllowAny, ]
        return [permission() for permission in permission_classes]