from django.db import models
from product_management.models import PRODUCT

# Create your models here.
class MENU(models.Model):

	#menu for browsing products for cart
	productId = models.ForeignKey(PRODUCT, on_delete=models.CASCADE)
	
	#track the quantity to buy of the specific product
	itemQuantAdded = models.IntegerField()

	#get the total of the product that was purchased(itemQuantAdded*productPrice)
	itemTotal = models.DecimalField(max_digits=10, decimal_places=2)