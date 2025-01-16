from django.urls import path
from . import views
urlpatterns = [
	path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register_view, name='register'),
    path('success', views.success_page, name='success'),

	path('users/', views.UserAPI.as_view()),  # GET (all users), POST (create user)
    path('users/<int:pk>/', views.UserAPI.as_view()),  # GET (specific user), PUT, DELETE
]
