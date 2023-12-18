from django.urls import path

from .views import UserLoginView, UserLogoutView, UserRegisterView

app_name = 'user'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='account_login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register')
]
