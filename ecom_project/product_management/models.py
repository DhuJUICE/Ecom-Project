from django.db import models

# Create your models here.
class PRODUCT(models.Model):

	#product details for database
	prodName = models.CharField(max_length = 100)
	prodPrice = models.DecimalField(max_digits=10, decimal_places=2)
	prodDesc = models.CharField(max_length = 100)
	prodAvailQuant = models.IntegerField()
	prodOnMenu =  models.BooleanField(default=False)