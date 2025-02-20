from django.urls import path
from . import views
urlpatterns = [
	path('checkout-page', views.DisplayPage),
	path('checkout/', views.CheckoutTrackingView.as_view(), name='checkout-list'),
    path('checkout/<int:transaction_id>/', views.CheckoutTrackingView.as_view(), name='checkout-detail'),
	path('checkout/add/', views.add_first_cart_item_to_transaction, name='add_first_cart_item_to_transaction'),
    path('', views.displayTemplate, name='first_cart_item_to_transaction'),
]
