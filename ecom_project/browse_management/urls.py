from django.urls import path
from . import views
urlpatterns = [
	path('browse', views.DisplayPage),
	path('get-menu-items/', views.get_menu_items, name='get_menu_items'),
]
