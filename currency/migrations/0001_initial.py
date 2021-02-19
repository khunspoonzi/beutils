# Generated by Django 3.1.1 on 2021-02-18 09:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("beutils_location", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Currency",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="created at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="updated at"),
                ),
                (
                    "name",
                    models.CharField(max_length=255, unique=True, verbose_name="name"),
                ),
                (
                    "slug",
                    models.CharField(
                        blank=True, max_length=255, unique=True, verbose_name="slug"
                    ),
                ),
                ("name_plural", models.CharField(max_length=255)),
                ("code", models.CharField(max_length=10, unique=True)),
                (
                    "number",
                    models.PositiveIntegerField(unique=True, blank=True, null=True),
                ),
                ("symbol", models.CharField(max_length=5)),
                ("symbol_native", models.CharField(max_length=20)),
                (
                    "kind",
                    models.CharField(
                        choices=[("crypto", "Crypto"), ("fiat", "Fiat")], max_length=10
                    ),
                ),
                (
                    "country",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="currencies",
                        to="beutils_location.country",
                        blank=True,
                        null=True,
                    ),
                ),
            ],
            options={
                "verbose_name": "Currency",
                "verbose_name_plural": "Currencies",
            },
        ),
    ]
