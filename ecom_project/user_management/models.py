from django.db import models

# Create your models here.
class user(models.Model):
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
    ]

    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30)  
    last_name = models.CharField(max_length=30)   
    email_address = models.EmailField(unique=True)
    role = models.CharField(
        max_length=10, 
        choices=ROLE_CHOICES, 
        default='customer'
    )

    def __str__(self):
        return self.first_name + " " + self.last_name + " " + self.email_address + " " + self.role