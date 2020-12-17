from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Set paths for login, logout, and create account views
    path('', views.loginPage, name='loginPage'),
    path('logout/', views.logoutUser, name="logout"),
    path('createAccount/', views.createAccount, name='createAccount'),

    # Sets paths for Django's built in reset password views
    # Used when selecting forgot password on login page
    path('password_reset/',
         auth_views.PasswordResetView.as_view(
             template_name="account/ForgotPassword.html"),
         name="password_reset"),
    path('password_reset_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name="account/PasswordResetSent.html"),
        name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="account/CreateNewPassword.html"),
        name="password_reset_confirm"),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name="account/PasswordResetDone.html"),
        name="password_reset_complete"),
]
