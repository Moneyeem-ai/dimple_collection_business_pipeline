# Generated by Django 4.2.7 on 2023-12-22 09:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0007_alter_product_image_alter_product_tag_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="brand",
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name="product",
            name="category",
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name="product",
            name="color",
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name="product",
            name="department",
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name="product",
            name="subcategory",
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.DeleteModel(
            name="Brand",
        ),
        migrations.DeleteModel(
            name="Color",
        ),
    ]
