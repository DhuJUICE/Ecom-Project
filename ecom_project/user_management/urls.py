from django.urls import path
from . import views
urlpatterns = [
	path('sign', views.SignUpPage),
	path('login', views.LoginPage)
]
