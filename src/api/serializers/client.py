from rest_framework import serializers

from api.models.client import ClientModel


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientModel
        fields = "__all__"
