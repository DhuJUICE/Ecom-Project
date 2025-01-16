from django.urls import path
from . import views
urlpatterns = [
	path('product', views.DisplayPage),
	path('products/', views.ProductAPI.as_view()),  # For GET (all) and POST
    path('products/<int:pk>/', views.ProductAPI.as_view()),  # For GET (by ID), PUT, DELETE
]
