# Generated by Django 5.1.4 on 2024-12-07 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(default='customer', max_length=30),
        ),
    ]
