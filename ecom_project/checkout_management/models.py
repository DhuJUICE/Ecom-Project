from django.db import models
from cart_management.models import CART

# Create your models here.
class TRANSACTION_LOG(models.Model):
	#add cart menu products to the transaction log for keeping track of what was actually sold
	cartId = models.ForeignKey(CART, on_delete=models.CASCADE)