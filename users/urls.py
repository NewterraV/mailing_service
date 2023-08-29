from django.urls import path

from users.apps import UsersConfig
from users.views import LoginView, LogoutView, RegisterView, reset_password, VerifyUpdateView, UserUpdateView


app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('verify/<int:pk>', VerifyUpdateView.as_view(), name='verify'),
    path('update/', UserUpdateView.as_view(), name='update'),
    path('reset-password/', reset_password, name='reset_password'),
]
