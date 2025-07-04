# Generated by Django 4.2.9 on 2024-01-11 13:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0015_alter_ptfileentry_quantity"),
    ]

    operations = [
        migrations.CreateModel(
            name="Genre",
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
                ("name", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Movie",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=255)),
                ("director", models.CharField(max_length=255)),
                ("release_date", models.DateField()),
                ("parents_guide", models.BooleanField()),
                ("imdb_rating", models.DecimalField(decimal_places=2, max_digits=4)),
                ("imdb_link", models.URLField()),
                ("genre", models.ManyToManyField(to="product.genre")),
            ],
        ),
    ]
