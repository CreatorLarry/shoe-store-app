# Generated by Django 5.1.7 on 2025-05-23 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_size_remove_product_size_product_sizes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='sizes',
        ),
        migrations.AddField(
            model_name='product',
            name='sizes',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
