# Generated by Django 4.1.3 on 2023-12-17 18:32

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0002_alter_product_size_alter_productquantity_quantity"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="ProductBarcode",
            new_name="Barcode",
        ),
    ]
