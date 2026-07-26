from django.urls import path, include
from dj_rest_auth.views import PasswordResetConfirmView
from . import views

urlpatterns = [
    path("user/", views.UserDetailsView.as_view() , name="user_details"),
    path("", include("dj_rest_auth.urls")),
    path("registration/" , include("dj_rest_auth.registration.urls")),
    path("password/reset/confirm/<uidb64>/<token>/" , PasswordResetConfirmView.as_view(), name="password_reset_confirm")
]