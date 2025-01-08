# Generated by Django 5.1.4 on 2024-12-07 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0002_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('customer', 'Customer'), ('staff', 'Staff'), ('admin', 'Admin')], default='customer', max_length=10),
        ),
    ]
