from rest_framework.viewsets import ModelViewSet

from sgz.users.permissions import IsOwnerUser
from sgz.utils.mixins import PaginatedCustomOrderingMixin


class BaseSGZViewSet(PaginatedCustomOrderingMixin, ModelViewSet):
    pass


class OwnerSGZViewSet(BaseSGZViewSet):
    permission_classes = [IsOwnerUser]
