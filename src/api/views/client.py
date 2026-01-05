from rest_framework.viewsets import ModelViewSet

from api.serializers.client import ClientSerializer


class ClientsView(ModelViewSet):
    serializer_class = ClientSerializer

    def get_queryset(self):
        return super().get_queryset()
