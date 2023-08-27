from django.urls import path
from .views import SignupView, LoginView, ResetPasswordView, ForgotPasswordView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),




]
