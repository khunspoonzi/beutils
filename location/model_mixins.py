# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │DJANGO IMPORTS                                                                      │
# └────────────────────────────────────────────────────────────────────────────────────┘

from django.db import models

# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │PROJECT IMPORTS                                                                     │
# └────────────────────────────────────────────────────────────────────────────────────┘

from beutils.location.models import City, Country, Region, State, Subregion

# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │LOCATION MODEL MIXIN                                                                │
# └────────────────────────────────────────────────────────────────────────────────────┘


class LocationModelMixin(models.Model):
    """ Location Model Mixin """

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │REGION                                                                          │
    # └────────────────────────────────────────────────────────────────────────────────┘

    region = models.ForeignKey(Region, blank=True, null=True, on_delete=models.PROTECT)

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │SUBREGION                                                                       │
    # └────────────────────────────────────────────────────────────────────────────────┘

    subregion = models.ForeignKey(
        Subregion, blank=True, null=True, on_delete=models.PROTECT
    )

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │COUNTRY                                                                         │
    # └────────────────────────────────────────────────────────────────────────────────┘

    country = models.ForeignKey(
        Country, blank=True, null=True, on_delete=models.PROTECT
    )

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │STATE                                                                           │
    # └────────────────────────────────────────────────────────────────────────────────┘

    state = models.ForeignKey(State, blank=True, null=True, on_delete=models.PROTECT)

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │CITY                                                                            │
    # └────────────────────────────────────────────────────────────────────────────────┘

    city = models.ForeignKey(City, blank=True, null=True, on_delete=models.PROTECT)

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │SAVE                                                                            │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def save(self, *args, **kwargs):
        """ Custom Save Method """

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ PRE-SAVE UPDATED                                                           │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Check if city is defined
        if self.city:

            # Syncronize parent foreign keys
            self.region_id = self.city.state.country.subregion.region_id
            self.subregion_id = self.city.state.country.subregion_id
            self.country_id = self.city.state.country_id
            self.state_id = self.city.state_id

        # Otherwise, check if state is defined
        elif self.state:

            # Syncronize parent foreign keys
            self.region_id = self.state.country.subregion.region_id
            self.subregion_id = self.state.country.subregion_id
            self.country_id = self.state.country_id

        # Otherwise, check if country is defined
        elif self.country:

            # Syncronize parent foreign keys
            self.region_id = self.country.subregion.region_id
            self.subregion_id = self.country.subregion_id

        # Otherwise, check if subregion is defined
        elif self.subregion:

            # Syncronize parent foreign keys
            self.region_id = self.subregion.region_id

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ SAVE OBJECT                                                                │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Save object
        super().save(*args, **kwargs)

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │META                                                                            │
    # └────────────────────────────────────────────────────────────────────────────────┘

    class Meta:

        # Set abstract to True
        abstract = True
