# Generated by Django 5.0.6 on 2025-01-14 21:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MENU',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('itemQuantAdded', models.IntegerField()),
                ('itemTotal', models.DecimalField(decimal_places=2, max_digits=10)),
                ('productId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_management.product')),
            ],
        ),
    ]
