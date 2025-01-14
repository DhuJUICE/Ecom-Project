from django.db import models
from browse_management.models import MENU
from django.contrib.auth.models import User, auth

# Create your models here.
class CART(models.Model):
	#user details for cart table in database - as foreign key to get values from User table
	userId = models.ForeignKey(User, on_delete=models.CASCADE)
	
	#product details for cart in database - - as foreign key to get values from PRODUCT table
	menuId = models.ForeignKey(MENU, on_delete=models.CASCADE)

	#track the date and time the product was added to the cart
	datetimeAdded = models.DateTimeField()
