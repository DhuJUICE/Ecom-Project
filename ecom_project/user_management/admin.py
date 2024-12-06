from django.contrib import admin
from .models import user  # Import your user model

@admin.register(user)  # Register the model with a decorator
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'first_name', 'last_name', 'email_address')  # Columns to display
    search_fields = ('first_name', 'last_name', 'email_address')  # Search functionality
    list_filter = ('first_name',)  # Add filters if needed

