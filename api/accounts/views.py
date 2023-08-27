import random
import string
from rest_framework import generics, status
from .users.users_serializers import UserSerializer, ResetPasswordSerializer, Forgotpasswordserializer, LoginSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .users.user_models import User
from .controller import UserController


#signup
class SignupView(generics.CreateAPIView):
    serializer_class = UserSerializer  


class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer  # Use your LoginSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(email=email, password=password)
        if user is None:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        return Response({
            'access_token': str(access_token),
            'refresh_token': str(refresh),
            'full_name': user.full_name,
        })


class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'error': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)

            new_password = request.new_password
            user.set_password(new_password)
            instance = user.save()
            UserController.send_reset_password_mail(instance)            

            return Response({'message': 'Password reset instructions sent successfully'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(generics.GenericAPIView):
    serializer_class = Forgotpasswordserializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'message': 'No user found with this email'}, status=status.HTTP_404_NOT_FOUND)

        new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        user.set_password(new_password)
        instance = user.save()
        UserController.send_forgot_password_mail(instance, new_password)

        return Response({'message': "New password sent successfully"}, status=status.HTTP_202_ACCEPTED)
