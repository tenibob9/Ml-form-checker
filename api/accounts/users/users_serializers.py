from rest_framework import serializers
from .user_models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'full_name' , 'role')
        extra_kwargs = {
            'password': {'write_only': True}, 
            'email': {'required': True},
            # 'is_staff': {'required': True}, 
            'role': {'required': True},     
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.is_active
        user.save()
        return user

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField(max_length=255)

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError('User with this email does not exist')
        return value

class Forgotpasswordserializer(serializers.Serializer):
    email = serializers.EmailField()

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
