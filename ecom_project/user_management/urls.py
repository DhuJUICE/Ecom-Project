from django.urls import path
from . import views
urlpatterns = [
	path('sigin', views.SignUpPage, name='sign-in'),
	path('login', views.LoginPage, name='login'),
    path('register', views.register, name='register'),
]
