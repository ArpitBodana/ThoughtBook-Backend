from django.urls import path
from . import views 
from knox import views as knox_views


urlpatterns=[
    path('',views.home,name="home"),
    path('api/v1/register/', views.RegisterAPI.as_view(), name='register'),
    path('api/login/', views.LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('api/change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    
   

]