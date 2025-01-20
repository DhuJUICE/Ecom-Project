from django.urls import path
from . import views

#token view imports
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
	path('api', views.DisplayPage),
	path('api/token', TokenObtainPairView.as_view(), name='token'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token-refresh'),
]
