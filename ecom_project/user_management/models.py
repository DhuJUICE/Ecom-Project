from django.db import models

# Create your models here.
class user(models.Model):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30)  
    last_name = models.CharField(max_length=30)   
    email_address = models.EmailField(unique=True)

    def __str__(self):
        return self.first_name + " " + self.last_name + " " + self.email_address