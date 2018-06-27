from django.http import HttpResponse
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


# import jwt, json
# from rest_framework import views
# from rest_framework.response import Response
#
#
# class Login(views.APIView):
#
#     def post(self, request, *args, **kwargs):
#         if not request.data:
#             return Response({'Error': "Please provide username/password"}, status="400")
#
#         username = request.data.get('username')
#         password = request.data.get('password')
#         try:
#             user = User.objects.get(username=username, password=password)
#         except User.DoesNotExist:
#             return Response({'Error': "Invalid username/password"}, status="400")
#         if user:
#             payload = {
#                 'id': user.id,
#                 'email': user.email,
#             }
#             jwt_token = {'token': jwt.encode(payload, "SECRET_KEY")}
#
#             return HttpResponse(
#                 json.dumps(jwt_token),
#                 status=200,
#                 content_type="application/json"
#             )
#         else:
#             return Response(
#                 json.dumps({'Error': "Invalid credentials"}),
#                 status=400,
#                 content_type="application/json"
#             )