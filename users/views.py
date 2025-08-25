from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import User
from .serializers import UserSerializer
import random
# Create your views here.


class RegisterView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        ism = request.data.get("ism")
        bio = request.data.get("bio")

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already taken"}, status=400)


        code = str(random.randint(1000, 9999))

        user = User.objects.create_user(
            username=username,
            password=password,
            ism=ism,
            bio=bio
        )
        user.code = code   
        user.save()        

        return Response({"msg": "User created", "code": code}, status=201)

class VerifyCodeView(APIView):
    def post(self, request):
        username = request.data.get("username")
        code = request.data.get("code")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        if user.code == code:
            return Response({"msg": "Verified!"}, status=200)
        return Response({"error": "Invalid code"}, status=400)

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
