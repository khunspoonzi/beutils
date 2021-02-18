# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ DJANGO IMPORTS                                                                     │
# └────────────────────────────────────────────────────────────────────────────────────┘

from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.db import models

# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ PROJECT IMPORTS                                                                    │
# └────────────────────────────────────────────────────────────────────────────────────┘

from beutils.model_mixins import (
    EmojiModelMixin,
    NameSlugModelMixin,
    TimeStampedModelMixin,
    UniqueNameSlugModelMixin,
)
from beutils.tools import slugify


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ REGION                                                                             │
# └────────────────────────────────────────────────────────────────────────────────────┘


class Region(UniqueNameSlugModelMixin, EmojiModelMixin, TimeStampedModelMixin):
    """ Region Model """

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ META                                                                           │
    # └────────────────────────────────────────────────────────────────────────────────┘

    class Meta:

        # Define verbose names
        verbose_name = "Region"
        verbose_name_plural = "Regions"


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ SUBREGION                                                                          │
# └────────────────────────────────────────────────────────────────────────────────────┘


class Subregion(UniqueNameSlugModelMixin, TimeStampedModelMixin):
    """ Subregion Model """

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ REGION FOREIGN KEY                                                             │
    # └────────────────────────────────────────────────────────────────────────────────┘

    region = models.ForeignKey(
        Region, related_name="subregions", on_delete=models.CASCADE
    )

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ META                                                                           │
    # └────────────────────────────────────────────────────────────────────────────────┘

    class Meta:

        # Define verbose names
        verbose_name = "Subregion"
        verbose_name_plural = "Subregions"


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ COUNTRY                                                                            │
# └────────────────────────────────────────────────────────────────────────────────────┘


class Country(UniqueNameSlugModelMixin, EmojiModelMixin, TimeStampedModelMixin):
    """ Country Model """

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ REGION FOREIGN KEY                                                             │
    # └────────────────────────────────────────────────────────────────────────────────┘

    region = models.ForeignKey(
        Region, related_name="countries", on_delete=models.CASCADE
    )

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ SUBREGION FOREIGN KEY                                                          │
    # └────────────────────────────────────────────────────────────────────────────────┘

    subregion = models.ForeignKey(
        Subregion, related_name="countries", on_delete=models.CASCADE
    )

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ CURRENCY FOREIGN KEY                                                           │
    # └────────────────────────────────────────────────────────────────────────────────┘

    # currency = models.ForeignKey(
    #     "currency.Currency",
    #     related_name="countries",
    #     on_delete=models.PROTECT,
    #     blank=True,
    #     null=True,
    # )

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ NAME OFFICIAL                                                                  │
    # └────────────────────────────────────────────────────────────────────────────────┘

    name_official = models.CharField(
        max_length=255,
        unique=True,
        blank=True,
    )

    slug_official = models.CharField(
        max_length=255,
        unique=True,
        blank=True,
    )

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ NAME NATIVE                                                                    │
    # └────────────────────────────────────────────────────────────────────────────────┘

    name_native = models.CharField(
        max_length=255,
        unique=True,
        blank=True,
    )

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ ISO CODES                                                                      │
    # └────────────────────────────────────────────────────────────────────────────────┘

    iso2 = models.CharField(max_length=2, unique=True)

    iso3 = models.CharField(max_length=3, unique=True)

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ PHONE CODES                                                                    │
    # └────────────────────────────────────────────────────────────────────────────────┘

    phone_codes = ArrayField(ArrayField(models.CharField(max_length=5)), default=list)

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ DEMONYM AND NATIONALITY                                                        │
    # └────────────────────────────────────────────────────────────────────────────────┘

    demonym = models.CharField(max_length=255)

    is_nationality = models.BooleanField()

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ SAVE                                                                           │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def save(self, *args, **kwargs):
        """ Custom Save Method """

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ PRE-SAVE UPDATED                                                           │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Iterate over non-null fields
        for field, display in (
            (self.name, "name"),
            (self.name_official, "official name"),
            (self.name_native, "native name"),
            (self.iso2, "iso2"),
            (self.iso3, "iso3"),
        ):

            # Check if field is null
            if not field:

                # Raise ValidationError
                raise ValidationError(f"{display.title()} cannot be an empty string")

        # Ensure that name and official name slugs are lowercased
        self.slug = slugify(self.name)
        self.slug_official = slugify(self.name_official)

        # Ensure that ISO2 and ISO3 alpha codes are uppercase
        self.iso2 = self.iso2.upper().strip()
        self.iso3 = self.iso3.upper().strip()

        # Synchronize parent foreign keys
        self.region_id = self.subregion.region_id

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ SAVE OBJECT                                                                │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Save object
        super().save(*args, **kwargs)

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ META                                                                           │
    # └────────────────────────────────────────────────────────────────────────────────┘

    class Meta:

        # Define verbose names
        verbose_name = "Country"
        verbose_name_plural = "Countries"


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ STATE                                                                              │
# └────────────────────────────────────────────────────────────────────────────────────┘


class State(NameSlugModelMixin, TimeStampedModelMixin):
    """ State Model """

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ REGION FOREIGN KEY                                                             │
    # └────────────────────────────────────────────────────────────────────────────────┘

    region = models.ForeignKey(Region, related_name="states", on_delete=models.CASCADE)

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ SUBREGION FOREIGN KEY                                                          │
    # └────────────────────────────────────────────────────────────────────────────────┘

    subregion = models.ForeignKey(
        Subregion, related_name="states", on_delete=models.CASCADE
    )

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ COUNTRY FOREIGN KEY                                                            │
    # └────────────────────────────────────────────────────────────────────────────────┘

    country = models.ForeignKey(
        Country, related_name="states", on_delete=models.CASCADE
    )

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ SAVE                                                                           │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def save(self, *args, **kwargs):
        """ Custom Save Method """

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ PRE-SAVE UPDATED                                                           │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Syncronize parent foreign keys
        self.region_id = self.country.subregion.region_id
        self.subregion_id = self.country.subregion_id

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ SAVE OBJECT                                                                │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Save object
        super().save(*args, **kwargs)

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ META                                                                           │
    # └────────────────────────────────────────────────────────────────────────────────┘

    class Meta:

        # Define verbose names
        verbose_name = "State"
        verbose_name_plural = "States"


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ CITY                                                                               │
# └────────────────────────────────────────────────────────────────────────────────────┘


class City(NameSlugModelMixin, TimeStampedModelMixin):
    """ City Model """

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ REGION FOREIGN KEY                                                             │
    # └────────────────────────────────────────────────────────────────────────────────┘

    region = models.ForeignKey(Region, related_name="cities", on_delete=models.CASCADE)

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ SUBREGION FOREIGN KEY                                                          │
    # └────────────────────────────────────────────────────────────────────────────────┘

    subregion = models.ForeignKey(
        Subregion, related_name="cities", on_delete=models.CASCADE
    )

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ COUNTRY FOREIGN KEY                                                            │
    # └────────────────────────────────────────────────────────────────────────────────┘

    country = models.ForeignKey(
        Country, related_name="cities", on_delete=models.CASCADE
    )

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ STATE FOREIGN KEY                                                              │
    # └────────────────────────────────────────────────────────────────────────────────┘

    state = models.ForeignKey(State, related_name="cities", on_delete=models.CASCADE)

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ SAVE                                                                           │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def save(self, *args, **kwargs):
        """ Custom Save Method """

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ PRE-SAVE UPDATED                                                           │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Syncronize parent foreign keys
        self.region_id = self.state.country.subregion.region_id
        self.subregion_id = self.state.country.subregion_id
        self.country_id = self.state.country_id

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ SAVE OBJECT                                                                │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Save object
        super().save(*args, **kwargs)

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ META                                                                           │
    # └────────────────────────────────────────────────────────────────────────────────┘

    class Meta:

        # Define verbose names
        verbose_name = "City"
        verbose_name_plural = "Cities"
