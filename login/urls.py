from django.urls import path
from . import views
from . import views

app_name = 'users'
urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.LogoutUser.as_view(), name='logout'),
    path('register/', views.Register.as_view(), name='register'),
    path('', views.Dashboard.as_view(), name='dashboard'),

]