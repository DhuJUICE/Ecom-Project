# Generated by Django 5.1.4 on 2024-12-08 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0004_user_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=128),
        ),
    ]