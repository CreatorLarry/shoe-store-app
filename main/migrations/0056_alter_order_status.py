# Generated by Django 5.1.7 on 2025-06-19 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0055_sale_email_sale_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, choices=[('pending', 'Pending'), ('paid & picked', 'Paid & Picked')], default='pending', max_length=50, null=True),
        ),
    ]
