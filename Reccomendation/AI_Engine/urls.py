from django.urls import path,include
from . import views
from .import AIviews


urlpatterns = [
    path('register/',views.register,name="register_user"),
    path('profile/',views.profile,name="profile"),
    path('login/',views.login_view,name="login_user"),
    path('logout/',views.logout_view,name="logout_user"),
    path('AI-result/',AIviews.AI_view,name="Reccomendations"),
    
]
