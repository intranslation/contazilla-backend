from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from api.serializers.client import ClientSerializer
from api.models import Client


class ClientsView(ModelViewSet):
    # class ClientsView(GenericViewSet, ListModelMixin, CreateModelMixin):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    permission_classes = [IsAuthenticated]
