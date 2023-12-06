from django.urls import path
from . import views
from django.contrib.auth.views import LoginView,LogoutView



urlpatterns = [
    path('',views.index,name='index'),
    path('signup/',views.signup,name='signup'),
    path('login/',LoginView.as_view(template_name = 'login.html'),name='login'),
    path('logout/',LogoutView.as_view(template_name = 'logout.html'),name='logout'),
    path('chat/<int:user_id>/',views.chat,name='chat'),
    path('profile/<str:username>/',views.profile,name='profile'),
    path('profile/user/edit/',views.profile_update,name='update_profile'),
    path('profile/user/password/',views.ChangePasswordView.as_view(),name='password_change')
]
