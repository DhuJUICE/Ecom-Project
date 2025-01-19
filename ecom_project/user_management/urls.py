from django.urls import path
from . import views

urlpatterns = [
	#User Login urls
	path('login-page', views.displayLogin, name='login-page'),
	path('login-function', views.login_view, name='login-function'),

	#User SignUp/Register urls
    path('register-page', views.displayRegister, name='register-page'),
	path('register-function', views.register_view, name='register-function'),

	#User Logout url
	path('logout', views.logout_view, name='logout'),

	#USERS API ENDPOINT
	path('users/', views.UserAPI.as_view()),  # GET (all users), POST (create user)
    path('users/<int:pk>/', views.UserAPI.as_view()),  # GET (specific user), PUT, DELETE
]
