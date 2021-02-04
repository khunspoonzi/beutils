# -------------------------------------------------------------------------------------
# DJANGO IMPORTS
# -------------------------------------------------------------------------------------

from django.db.models import Case, CharField, F, Q, Value, When
from django.db.models.functions import Concat


# -------------------------------------------------------------------------------------
# LOCATION MODEL VIEWSET MIXIN
# -------------------------------------------------------------------------------------


class LocationModelViewSetMixin:
    """ A viewset mixin for models with location fields """

    # ---------------------------------------------------------------------------------
    # FILTER QUERYSET
    # ---------------------------------------------------------------------------------

    def filter_queryset(self, queryset):
        """ Calls annotate location on the current queryset """

        # Call parent filter queryset method
        queryset = super().filter_queryset(queryset)

        # Annotate location into queryset
        return self.annotate_location(queryset)

    # ---------------------------------------------------------------------------------
    # ANNOTATE LOCATION
    # ---------------------------------------------------------------------------------

    def annotate_location(
        self, queryset, default="Unspecified", variant=4, mirror_variant=False
    ):
        """
        Annotates a location string based on the model's location foreign key fields
        """

        # -----------------------------------------------------------------------------
        # VARIABLES
        # -----------------------------------------------------------------------------

        # Get comma string
        comma = Value(", ")

        # Get location fields
        region_field = "region__name"
        subregion_field = "subregion__name"
        country_field = "country__name"
        state_field = "state__name"
        city_field = "city__name"

        # -----------------------------------------------------------------------------
        # CITY
        # -----------------------------------------------------------------------------

        # Initialize city preconditions
        city_pre_conditions = []

        # Handle case of variants 3 and 5
        if variant in [3, 5]:

            # Define city components
            city_components = [
                country_field,
                comma,
                city_field,
            ]

            # Define pre-condition for country == city --> Omit city
            city_pre_conditions.append(
                When(
                    city__isnull=False,
                    city__name=F("country__name"),
                    then=F(country_field),
                ),
            )

        # Otherwise handle all other cases
        else:

            # Define city components
            city_components = [
                region_field,
                comma,
                subregion_field,
                comma,
                country_field,
                comma,
                state_field,
                comma,
                city_field,
            ]

            # Otheriwse, handle case of variants 2 and 4
            if variant in [2, 4]:

                # Redefine city components: remove region and subregion
                city_components = city_components[4:]

            # -------------------------------------------------------------------------
            # HANDLE REDUNDANCY: COUNTRY == STATE == CITY
            # -------------------------------------------------------------------------

            # Define city pre-components: remove state and city
            city_pre_components = city_components[:-4]
            city_pre_components = (
                city_pre_components[::-1] if mirror_variant else city_pre_components
            )

            # Define pre-condition for country == state == city
            city_pre_conditions.append(
                When(
                    Q(city__isnull=False)
                    & Q(city__name=F("state__name"))
                    & Q(city__name=F("country__name")),
                    then=Concat(*city_pre_components)
                    if len(city_pre_components) > 1
                    else F(*city_pre_components),
                ),
            )

            # -------------------------------------------------------------------------
            # HANDLE REDUNDANCY: STATE == CITY
            # -------------------------------------------------------------------------

            # Define city pre-components, i.e. remove city
            city_pre_components = city_components[:-2]
            city_pre_components = (
                city_pre_components[::-1] if mirror_variant else city_pre_components
            )

            # Define pre-condition for state == city
            city_pre_conditions.append(
                When(
                    city__isnull=False,
                    city__name=F("state__name"),
                    then=Concat(*city_pre_components),
                ),
            )

        # Mirror city components if necessary
        city_components = city_components[::-1] if mirror_variant else city_components

        # Define city condition
        city_condition = When(
            city__isnull=False,
            then=Concat(*city_components),
        )

        # -----------------------------------------------------------------------------
        # STATE
        # -----------------------------------------------------------------------------

        # Define state components
        state_components = [
            region_field,
            comma,
            subregion_field,
            comma,
            country_field,
            comma,
            state_field,
        ]

        # Handle case of variants 2 to 5
        if variant in [2, 3, 4, 5]:

            # Redefine state components: remove region and subregion
            state_components = state_components[4:]

        # Define state pre-components, i.e. remove state
        state_pre_components = state_components[:-2]
        state_pre_components = (
            state_pre_components[::-1] if mirror_variant else state_pre_components
        )

        # Define pre-condition for country == state
        state_pre_condition = When(
            state__isnull=False,
            state__name=F("country__name"),
            then=Concat(*state_pre_components)
            if len(state_pre_components) > 1
            else F(*state_pre_components),
        )

        # Mirror state components if necessary
        state_components = (
            state_components[::-1] if mirror_variant else state_components
        )

        # Define staet condition
        state_condition = When(
            state__isnull=False,
            then=Concat(*state_components),
        )

        # -----------------------------------------------------------------------------
        # COUNTRY
        # -----------------------------------------------------------------------------

        # Define country components
        country_components = [
            region_field,
            comma,
            subregion_field,
            comma,
            country_field,
        ]

        # Handle case of variants 2 to 5
        if variant in [2, 3, 4, 5]:

            # Redefine country components: remove region and subregion
            country_components = country_components[4:]

        # Mirror country components if necessary
        country_components = (
            country_components[::-1] if mirror_variant else country_components
        )

        # Define country condition
        country_condition = When(
            country__isnull=False,
            then=Concat(*country_components)
            if len(country_components) > 1
            else F(*country_components),
        )

        # -----------------------------------------------------------------------------
        # SUBREGION
        # -----------------------------------------------------------------------------

        # Define subregion components
        subregion_components = [
            region_field,
            comma,
            subregion_field,
        ]

        # Handle case of variants 4 and 5
        if variant in [4, 5]:

            # Redefine subregion components: remove region
            subregion_components = subregion_components[2:]

        # Mirror subregion components if necessary
        subregion_components = (
            subregion_components[::-1] if mirror_variant else subregion_components
        )

        # Define subregion condition
        subregion_condition = When(
            subregion__isnull=False,
            then=Concat(*subregion_components)
            if len(subregion_components) > 1
            else F(*subregion_components),
        )

        # -----------------------------------------------------------------------------
        # REGION
        # -----------------------------------------------------------------------------

        # Define region condition
        region_condition = When(
            region__isnull=False,
            then=F("region__name"),
        )

        # -----------------------------------------------------------------------------
        # ANNOTATE QUERYSET
        # -----------------------------------------------------------------------------

        # Annotate queryset
        queryset = queryset.annotate(
            location=Case(
                *city_pre_conditions,
                city_condition,
                state_pre_condition,
                state_condition,
                country_condition,
                subregion_condition,
                region_condition,
                default=Value(default),
                output_field=CharField(),
            )
        )

        # Return annotated queryset
        return queryset


# -------------------------------------------------------------------------------------
# LOCATION OPTIONS
# -------------------------------------------------------------------------------------

"""

Abbreviate States                  [x]
Abbreviate Countries w/ ISO 3      [x]
Abbreviate Countries w/ ISO 2      [x]
Default for null locations         [x]
Post conditions                    [x]
Mirror Variant                     [x]


"""

# -------------------------------------------------------------------------------------
# LOCATION VARIATIONS
# -------------------------------------------------------------------------------------

"""

Variation 1:

    Region, Subregion, Country, State, City
    Region, Subregion, Country, State
    Region, Subregion, Country
    Region, Subregion
    Region

Variation 2:

    Country, State, City
    Country, State
    Country
    Region, Subregion
    Region

Variation 3:

    Country, City
    Country, State
    Country
    Region, Subregion
    Region

Variation 4:

    Country, State, City
    Country, State
    Country
    Subregion
    Region

Variation 5:

    Country, City
    Country, State
    Country
    Subregion
    Region

Plus the mirrored versions of these variants

"""
