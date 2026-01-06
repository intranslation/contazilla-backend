from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import RegisterRequestSerializer


class RegisterView(APIView):
    @swagger_auto_schema(request_body=RegisterRequestSerializer)
    def post(self, request):
        serializer = RegisterRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        print(serializer.data)
        # User.objects.create(**serializer.data)

        return Response({"error": "Invalid credentials"}, status=400)
