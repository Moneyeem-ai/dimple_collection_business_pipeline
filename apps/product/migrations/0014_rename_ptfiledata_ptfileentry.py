# Generated by Django 4.2.9 on 2024-01-11 06:40

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0013_producttagimage_rename_color_product_hash_value_and_more"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="PTFileData",
            new_name="PTFileEntry",
        ),
    ]
