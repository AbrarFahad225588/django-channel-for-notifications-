from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth.models import User
class LoginSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):

        user = authenticate(
            username=attrs["username"],
            password=attrs["password"],
        )

        if not user:
            raise serializers.ValidationError("Invalid credentials")

        attrs["user"] = user
        return attrs

class UserSerializer(serializers.ModelSerializer):


    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'is_active',
            'first_name',
            'last_name',
            'date_joined'
        ]
        read_only_fields = fields


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
    )
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'password',
            'confirm_password',
        ]
    

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError(
                {'password': 'Passwords do not match.'}
            )
        return attrs
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value


    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        request = self.context.get('request')

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_active=True,
        )
        return user
    