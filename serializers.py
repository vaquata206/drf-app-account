import jwt
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Q
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token


class UserRegistrationSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        required=True,
        label="Email Address"
    )

    password = serializers.CharField(
        required=True,
        label="Password",
        style={'input_type': 'password'}
    )

    password_2 = serializers.CharField(
        required=True,
        label="Confirm Password",
        style={'input_type': 'password'}
    )

    first_name = serializers.CharField(
        required=True
    )

    last_name = serializers.CharField(
        required=True
    )

    class Meta(object):
        model = User
        fields = ['username', 'email', 'password', 'password_2', 'first_name', 'last_name']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def validate_password(self, value):
        if len(value) < getattr(settings, 'PASSWORD_MIN_LENGTH', 8):
            raise serializers.ValidationError(
                "Password should be atleast %s characters long." % getattr(settings, 'PASSWORD_MIN_LENGTH', 8)
            )
        return value

    def validate_password_2(self, value):
        data = self.get_initial()
        password = data.get('password')
        if password != value:
            raise serializers.ValidationError("Passwords doesn't match.")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def create(self, validated_data):
        username = validated_data.get('username')[0]
        email = validated_data.get('email')[0]
        password = validated_data.get('password')[0]
        first_name = validated_data.get('first_name')[0]
        last_name = validated_data.get('last_name')[0]

        User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        return validated_data


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    token = serializers.CharField(read_only=True)
    password = serializers.CharField(required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'token']

    def validate(self, data):
        password = data.get('password', None)
        username = data.get('username', None)

        user = User.objects.filter(username=username)

        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise serializers.ValidationError("This username/email is not valid.")

        if user_obj:
            if not user_obj.check_password(password):
                raise serializers.ValidationError("Invalid credentials.")

        if user_obj.is_active:
            payload = {
                'id': user_obj.id,
                'email': user_obj.email,
            }
            jwt_token = {'token': jwt.encode(payload, settings.SECRET_KEY)}
            data['token'] = jwt_token
        else:
            raise serializers.ValidationError("User not active.")

        return data
