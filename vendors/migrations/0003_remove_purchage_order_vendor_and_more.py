# Generated by Django 4.2.7 on 2023-11-21 16:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0002_vendors_average_response_time_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchage_order',
            name='vendor',
        ),
        migrations.DeleteModel(
            name='Historical_Performance',
        ),
        migrations.DeleteModel(
            name='Purchage_Order',
        ),
    ]
