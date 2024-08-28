from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from typing import Dict, Any
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework import generics


class LoginSerializer(TokenObtainPairSerializer):
    
    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        data = super().validate(attrs)

        refresh = self.get_token(self.user)
        data['tokens'] = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        data['user']={
            'username': self.user.username,
            'message': True
        }

        data.pop('refresh')
        data.pop('access')
        #data["refresh"] = str(refresh)
        #data["access"] = str(refresh.access_token)

        
        return data

class MyTokenObtain(TokenObtainPairView):
        serializer_class = LoginSerializer

class LogoutAPIView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserSerializer(serializers.ModelSerializer):
     password = serializers.CharField(write_only = True)

     class Meta:
          model = User
          fields = ('username', 'email', 'password')

     def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class TokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()


class RegisterAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        refresh = RefreshToken.for_user(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        
        return Response(data, status=status.HTTP_201_CREATED)
          