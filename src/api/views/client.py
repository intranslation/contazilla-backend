from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from api.serializers.client import ClientSerializer
from api.models import Client


class ClientsView(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]
