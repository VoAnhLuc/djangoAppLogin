from django.urls import path, include
from . import views

app_name = 'api'
urlpatterns = [

    path('', views.APIHome.as_view(), name='api'),
    path('users/sign_up', views.CreateUser.as_view(), name='sign_up'),
    path('users/login', views.Login.as_view(), name='login'),
]
