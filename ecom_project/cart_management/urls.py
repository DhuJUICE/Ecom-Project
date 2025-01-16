from django.urls import path
from . import views
urlpatterns = [
	path('cart-page', views.DisplayPage),
	path('cart/', views.CartManagementView.as_view(), name='cart-list-create'),  # GET all, POST
    path('cart/<int:cart_id>/', views.CartManagementView.as_view(), name='cart-detail'),  # GET, PUT, DELETE specific item
	path('cart/add/', views.AddToCartQuickView.as_view(), name='quick_add_to_cart'),
]
