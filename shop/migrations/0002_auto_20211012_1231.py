# Generated by Django 3.2.8 on 2021-10-12 09:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='purchaseorder',
            old_name='quantity',
            new_name='count',
        ),
        migrations.RenameField(
            model_name='purchaseorder',
            old_name='product',
            new_name='product_id',
        ),
    ]
