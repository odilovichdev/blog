from django.urls import path

from users.views import LoginView, RegisterView, Profile, LogoutView, EditProfile

app_name = 'users'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', Profile.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('edit/', EditProfile.as_view(), name='edit'),
]