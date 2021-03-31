from .views import *
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

urlpatterns =[
    path('register', RegistrationView.as_view(), name ="register"),
    path('login', LoginView.as_view(), name ="login"),
    path('logout',LogoutView.as_view(), name ='logout'),
    path('request_reset_link',RequestPasswordResetEmail.as_view(), name ='request_reset_link'),
    path('validate_username', csrf_exempt(UsernameValidationView.as_view()), name ="validate_username"),
    path('validate_email', csrf_exempt(EmailValidationView.as_view()), name ="validate_email"),
    path('activate/<uidb64>/<token>',VerificationView.as_view(), name ='activate'),
    path('reset_user_password/<uidb64>/<token>',CompletePasswordReset.as_view(), name ='reset_user_password')



]