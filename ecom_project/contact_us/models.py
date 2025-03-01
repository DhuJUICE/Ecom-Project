from django.db import models

class CONTACT_US(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    subject = models.CharField(max_length=200)
    message = models.TextField()

    """
    def __str__(self):
        return f"Contact Us submission from {self.first_name} {self.last_name}"
    """