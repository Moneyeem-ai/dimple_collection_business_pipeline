# Generated by Django 4.2.7 on 2023-12-22 11:23

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0011_alter_product_mrp_alter_product_size_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="product",
            old_name="image",
            new_name="product_image",
        ),
    ]
