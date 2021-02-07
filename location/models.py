# -------------------------------------------------------------------------------------
# DJANGO IMPORTS
# -------------------------------------------------------------------------------------

from django.db import models

# -------------------------------------------------------------------------------------
# PROJECT IMPORTS
# -------------------------------------------------------------------------------------

from beutils.model_mixins import (
    EmojiModelMixin,
    NameSlugModelMixin,
    TimeStampedModelMixin,
    UniqueNameSlugModelMixin,
)


# -------------------------------------------------------------------------------------
# REGION
# -------------------------------------------------------------------------------------


class Region(UniqueNameSlugModelMixin, EmojiModelMixin, TimeStampedModelMixin):
    """ Region Model """

    # ---------------------------------------------------------------------------------
    # META
    # ---------------------------------------------------------------------------------

    class Meta:

        # Define verbose names
        verbose_name = "Region"
        verbose_name_plural = "Regions"


# -------------------------------------------------------------------------------------
# SUBREGION
# -------------------------------------------------------------------------------------


class Subregion(UniqueNameSlugModelMixin, TimeStampedModelMixin):
    """ Subregion Model """

    # ---------------------------------------------------------------------------------
    # REGION FOREIGN KEY
    # ---------------------------------------------------------------------------------

    region = models.ForeignKey(
        Region, related_name="subregions", on_delete=models.CASCADE
    )

    # ---------------------------------------------------------------------------------
    # META
    # ---------------------------------------------------------------------------------

    class Meta:

        # Define verbose names
        verbose_name = "Subregion"
        verbose_name_plural = "Subregions"


# -------------------------------------------------------------------------------------
# COUNTRY
# -------------------------------------------------------------------------------------


class Country(UniqueNameSlugModelMixin, EmojiModelMixin, TimeStampedModelMixin):
    """ Country Model """

    # ---------------------------------------------------------------------------------
    # REGION FOREIGN KEY
    # ---------------------------------------------------------------------------------

    region = models.ForeignKey(
        Region, related_name="countries", on_delete=models.CASCADE
    )

    # ---------------------------------------------------------------------------------
    # SUBREGION FOREIGN KEY
    # ---------------------------------------------------------------------------------

    subregion = models.ForeignKey(
        Subregion, related_name="countries", on_delete=models.CASCADE
    )

    # ---------------------------------------------------------------------------------
    # SAVE
    # ---------------------------------------------------------------------------------

    def save(self, *args, **kwargs):
        """ Custom Save Method """

        # -----------------------------------------------------------------------------
        # PRE-SAVE UPDATED
        # -----------------------------------------------------------------------------

        # Syncronize parent foreign keys
        self.region_id = self.subregion.region_id

        # -----------------------------------------------------------------------------
        # SAVE OBJECT
        # -----------------------------------------------------------------------------

        # Save object
        super().save(*args, **kwargs)

    # ---------------------------------------------------------------------------------
    # META
    # ---------------------------------------------------------------------------------

    class Meta:

        # Define verbose names
        verbose_name = "Country"
        verbose_name_plural = "Countries"


# -------------------------------------------------------------------------------------
# STATE
# -------------------------------------------------------------------------------------


class State(NameSlugModelMixin, TimeStampedModelMixin):
    """ State Model """

    # ---------------------------------------------------------------------------------
    # REGION FOREIGN KEY
    # ---------------------------------------------------------------------------------

    region = models.ForeignKey(Region, related_name="states", on_delete=models.CASCADE)

    # ---------------------------------------------------------------------------------
    # SUBREGION FOREIGN KEY
    # ---------------------------------------------------------------------------------

    subregion = models.ForeignKey(
        Subregion, related_name="states", on_delete=models.CASCADE
    )

    # ---------------------------------------------------------------------------------
    # COUNTRY FOREIGN KEY
    # ---------------------------------------------------------------------------------

    country = models.ForeignKey(
        Country, related_name="states", on_delete=models.CASCADE
    )

    # ---------------------------------------------------------------------------------
    # SAVE
    # ---------------------------------------------------------------------------------

    def save(self, *args, **kwargs):
        """ Custom Save Method """

        # -----------------------------------------------------------------------------
        # PRE-SAVE UPDATED
        # -----------------------------------------------------------------------------

        # Syncronize parent foreign keys
        self.region_id = self.country.subregion.region_id
        self.subregion_id = self.country.subregion_id

        # -----------------------------------------------------------------------------
        # SAVE OBJECT
        # -----------------------------------------------------------------------------

        # Save object
        super().save(*args, **kwargs)

    # ---------------------------------------------------------------------------------
    # META
    # ---------------------------------------------------------------------------------

    class Meta:

        # Define verbose names
        verbose_name = "State"
        verbose_name_plural = "States"


# -------------------------------------------------------------------------------------
# CITY
# -------------------------------------------------------------------------------------


class City(NameSlugModelMixin, TimeStampedModelMixin):
    """ City Model """

    # ---------------------------------------------------------------------------------
    # REGION FOREIGN KEY
    # ---------------------------------------------------------------------------------

    region = models.ForeignKey(Region, related_name="cities", on_delete=models.CASCADE)

    # ---------------------------------------------------------------------------------
    # SUBREGION FOREIGN KEY
    # ---------------------------------------------------------------------------------

    subregion = models.ForeignKey(
        Subregion, related_name="cities", on_delete=models.CASCADE
    )

    # ---------------------------------------------------------------------------------
    # COUNTRY FOREIGN KEY
    # ---------------------------------------------------------------------------------

    country = models.ForeignKey(
        Country, related_name="cities", on_delete=models.CASCADE
    )

    # ---------------------------------------------------------------------------------
    # STATE FOREIGN KEY
    # ---------------------------------------------------------------------------------

    state = models.ForeignKey(State, related_name="cities", on_delete=models.CASCADE)

    # ---------------------------------------------------------------------------------
    # SAVE
    # ---------------------------------------------------------------------------------

    def save(self, *args, **kwargs):
        """ Custom Save Method """

        # -----------------------------------------------------------------------------
        # PRE-SAVE UPDATED
        # -----------------------------------------------------------------------------

        # Syncronize parent foreign keys
        self.region_id = self.state.country.subregion.region_id
        self.subregion_id = self.state.country.subregion_id
        self.country_id = self.state.country_id

        # -----------------------------------------------------------------------------
        # SAVE OBJECT
        # -----------------------------------------------------------------------------

        # Save object
        super().save(*args, **kwargs)

    # ---------------------------------------------------------------------------------
    # META
    # ---------------------------------------------------------------------------------

    class Meta:

        # Define verbose names
        verbose_name = "City"
        verbose_name_plural = "Cities"
