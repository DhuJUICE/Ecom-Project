# Generated by Django 5.1.6 on 2025-02-18 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart_management', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='datetimeUpdated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
