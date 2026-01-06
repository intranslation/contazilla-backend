from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response

from rest_framework.views import APIView
from django.contrib.auth import authenticate, login

from api.serializers import LoginResponseSerializer, LoginRequestSerializer


class LoginView(APIView):

    @swagger_auto_schema(
        request_body=LoginRequestSerializer, responses={200: LoginResponseSerializer}
    )
    def post(self, request):
        user = authenticate(
            request,
            username=request.data.get("username"),
            password=request.data.get("password"),
        )

        if user:
            login(request, user)
            return Response(
                {"status": "Logged in", "email": user.email, "username": user.username}
            )

        return Response({"error": "Invalid credentials"}, status=400)
