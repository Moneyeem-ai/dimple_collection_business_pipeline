# Generated by Django 4.2.9 on 2024-06-26 17:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0043_remove_ptfileentry_color_code"),
    ]

    operations = [
        migrations.AddField(
            model_name="ptfileentry",
            name="color_code",
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]
