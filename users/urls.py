from django.contrib.auth import views as auth_views
from django.urls import path

from users import views

app_name = 'users'

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('list/', views.ParticipantsListView.as_view(), name='list'),
    path(
        'profile/<int:pk>/',
        views.UserDetailView.as_view(),
        name='profile_with_pk'
    ),
    path(
        'edit-profile/',
        views.UserProfileEditView.as_view(),
        name='edit_profile'
    ),
    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='users/change_password.html',
            success_url='/users/login/'
        ),
        name='password_change'
    ),
]


