from django.urls import path
from . import views
urlpatterns = [
	path('browse', views.DisplayPage),
	path('menu', views.MenuItemsAPIView.as_view(), name='menu-items'),
	#path('menu/<int:pk>/', views.MenuItemsAPIView.as_view(), name='menu-items'),
]
