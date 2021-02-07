# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │DJANGO REST FRAMEWORK IMPORTS                                                       │
# └────────────────────────────────────────────────────────────────────────────────────┘

from drf_multiple_model.viewsets import ObjectMultipleModelAPIViewSet
from rest_framework import filters

# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │BEUTIL IMPORTS                                                                      │
# └────────────────────────────────────────────────────────────────────────────────────┘

from beutils.pagination import DefaultMultipleModelPagination

# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │APP IMPORTS                                                                         │
# └────────────────────────────────────────────────────────────────────────────────────┘

from beutils.location.models import City, Country, Region, State, Subregion
from beutils.location.serializers import (
    CitySerializer,
    CountrySerializer,
    RegionSerializer,
    StateSerializer,
    SubregionSerializer,
)

# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │LOCATION VIEWSET                                                                    │
# └────────────────────────────────────────────────────────────────────────────────────┘


class LocationViewSet(ObjectMultipleModelAPIViewSet):
    """
    A viewset for viewing locations,
    i.e. region, subregion, country, state, city
    """

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │CLASS ATTRIBUTES                                                                │
    # └────────────────────────────────────────────────────────────────────────────────┘

    # Define pagination class
    pagination_class = DefaultMultipleModelPagination

    # Apply search filter backend
    filter_backends = (filters.SearchFilter,)

    # Define search fields
    search_fields = [
        "name",
    ]

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │QUERYLIST                                                                       │
    # └────────────────────────────────────────────────────────────────────────────────┘

    querylist = [
        {
            "queryset": Model.objects.all(),
            "serializer_class": SerializerClass,
            "label": SerializerClass.get_plural_name(),
        }
        for Model, SerializerClass in (
            (Region, RegionSerializer),
            (Subregion, SubregionSerializer),
            (Country, CountrySerializer),
            (State, StateSerializer),
            (City, CitySerializer),
        )
    ]
