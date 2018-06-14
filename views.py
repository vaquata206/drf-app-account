import sys

from django.contrib.auth.models import User
from rest_framework import generics, permissions, views, status
from rest_framework.response import Response
from .serializers import UserLoginSerializer, UserRegistrationSerializer


class RegisterAPIView(generics.CreateAPIView):
    """this class define the create behavior of our rest api"""
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegistrationSerializer
    queryset = User.objects.all()


class UserLoginAPIView(views.APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
