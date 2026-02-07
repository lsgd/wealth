from django.urls import path

from . import views

urlpatterns = [
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/me/', views.CurrentUserView.as_view(), name='current_user'),
    path('auth/change-password/', views.PasswordChangeView.as_view(), name='change_password'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('user/', views.UserUpdateView.as_view(), name='user_update'),
]
