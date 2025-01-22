from django.db import models
from browse_management.models import MENU
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField

class CART(models.Model):
    # User details for cart table in database - as foreign key to get values from User table
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Store cart items with their quantities as a JSON object
    menuCartItems = JSONField(
        default=dict,
        help_text="Dictionary where keys are MENU item IDs and values are quantities"
    )
    
    # Track the date and time the cart was last updated
    datetimeUpdated = models.DateTimeField(auto_now=True)