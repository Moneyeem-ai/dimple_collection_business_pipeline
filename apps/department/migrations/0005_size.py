# Generated by Django 4.2.9 on 2024-04-25 19:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("department", "0004_brand_supplier_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="Size",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("size_value", models.CharField(max_length=64)),
                (
                    "department",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="department.department",
                    ),
                ),
            ],
        ),
    ]
