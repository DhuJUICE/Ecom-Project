from rest_framework import serializers
from product_management.models import PRODUCT
from browse_management.models import MENU
from cart_management.models import CART
from checkout_management.models import TRANSACTION_LOG
from django.contrib.auth.models import User

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = PRODUCT
        fields = '__all__'

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = MENU
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = CART
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TRANSACTION_LOG
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'