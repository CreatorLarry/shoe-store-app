# Generated by Django 5.1.7 on 2025-05-29 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_subcategory_product_subcategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='subcategory',
            name='display_image',
            field=models.ImageField(blank=True, null=True, upload_to='products/subcategories/'),
        ),
    ]
