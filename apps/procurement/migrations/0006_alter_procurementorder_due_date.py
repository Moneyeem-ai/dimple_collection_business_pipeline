# Generated by Django 4.2.9 on 2024-07-12 14:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("procurement", "0005_alter_procurementorder_due_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="procurementorder",
            name="due_date",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
