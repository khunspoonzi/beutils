# Generated by Django 3.1.1 on 2021-02-17 11:13


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ GENERAL IMPORTS                                                                    │
# └────────────────────────────────────────────────────────────────────────────────────┘

import os

# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ DJANGO IMPORTS                                                                     │
# └────────────────────────────────────────────────────────────────────────────────────┘

from django.db import migrations


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ BEUTIL IMPORTS                                                                     │
# └────────────────────────────────────────────────────────────────────────────────────┘

from beutils.tools import read_json, slugify


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ CREATE FIAT CURRENCIES                                                             │
# └────────────────────────────────────────────────────────────────────────────────────┘


def create_fiat_currencies(apps, schema_editor):
    """ Creates Currency objects of type fiat from currency fixtures """

    # Get Currency and Country models
    Currency = apps.get_model("beutils_currency", "Currency")
    Country = apps.get_model("beutils_location", "Country")

    # Define fixture directory
    file_directory = "beutils/currency/fixtures/"

    # Define currency file name
    file_name = "fiat.json"

    # Read currency fixture file
    currencies = read_json(os.path.join(file_directory, file_name))

    # Return if file not found
    if not currencies:
        return

    # Order currencies by name
    currencies = sorted(currencies, key=lambda x: slugify(x["name"]))

    # Get all countries
    countries = Country.objects.all().values_list("iso3", "id")
    countries = {iso3: pk for iso3, pk in countries if iso3}

    # Bulk create currencies
    Currency.objects.bulk_create(
        [
            Currency(
                country_id=countries.get(currency["country_iso3"], None),
                name=currency["name"],
                slug=slugify(currency["name"]),
                name_plural=currency["name_plural"],
                code=currency["code"],
                number=currency["number"],
                symbol=currency["symbol"],
                symbol_native=currency["symbol_native"],
                kind="fiat",
            )
            for currency in currencies
        ]
    )


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ MIGRATION                                                                          │
# └────────────────────────────────────────────────────────────────────────────────────┘


class Migration(migrations.Migration):

    dependencies = [
        ("beutils_currency", "0001_initial"),
        ("beutils_location", "0002_create_regions_subregions_countries"),
    ]

    operations = [migrations.RunPython(create_fiat_currencies)]
