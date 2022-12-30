from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from sgz.users.permissions import IsOwnerUser

from .serializers import UserCreateUpdateSerializer, UserSerializer

User = get_user_model()


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"
    permission_classes = [IsOwnerUser]

    def get_serializer_class(self):
        if self.action == "create" or self.action == "update":
            return UserCreateUpdateSerializer
        return UserSerializer

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = UserCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def retrieve(self, request, *args, username="", **kwargs):
        users = self.queryset.filter(
            Q(username__icontains=username) | Q(full_name__icontains=username)
        )
        serializer = self.serializer_class(users, many=True)
        return Response(serializer.data[:10])
