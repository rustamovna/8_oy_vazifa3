from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import CustomUser
from .serializers import UserSerializer
import random


class RegisterView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        ism = request.data.get("ism")
        bio = request.data.get("bio")

        if CustomUser.objects.filter(email=email).exists():
            return Response({"error": "Email already taken"}, status=400)

        code = str(random.randint(1000, 9999))

        user = CustomUser.objects.create_user(
            email=email,
            password=password,
            ism=ism,
            bio=bio
        )
        user.save()

        return Response({"msg": "User created", "code": code}, status=201)


class VerifyCodeView(APIView):
    def post(self, request):
        email = request.data.get("email")
        code = request.data.get("code")

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        return Response({"msg": "Verified!"}, status=200)


class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class UploadImageView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        request.user.image = request.data.get("image")
        request.user.save()
        return Response({"msg": "Image uploaded"}, status=200)
