from django.db import models
from product_management.models import PRODUCT

# Create your models here.
class MENU(models.Model):

	#menu for browsing products for cart
	productId = models.ForeignKey(PRODUCT, on_delete=models.CASCADE)