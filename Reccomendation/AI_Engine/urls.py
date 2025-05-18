from django.urls import path,include
from . import views


urlpatterns = [
    path('register/',views.register,name="register_user"),
    path('profile/',views.profile,name="profile"),
    path('login/',views.login_view,name="login_user"),
    
]
