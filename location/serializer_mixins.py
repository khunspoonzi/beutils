# -------------------------------------------------------------------------------------
# DJANGO REST FRAMEWORK IMPORTS
# -------------------------------------------------------------------------------------

from dynamic_rest.fields import DynamicRelationField
from dynamic_rest.serializers import DynamicModelSerializer

# -------------------------------------------------------------------------------------
# PROJECT IMPORTS
# -------------------------------------------------------------------------------------

from beutils.location.serializers import (
    CitySerializer,
    CountrySerializer,
    RegionSerializer,
    StateSerializer,
    SubregionSerializer,
)


# -------------------------------------------------------------------------------------
# LOCATION DYNAMIC RELATION SERIALIZER MIXIN
# -------------------------------------------------------------------------------------


class LocationDynamicRelationSerializerMixin(DynamicModelSerializer):
    """ A serializer mixin for model serializers with sideloaded location fields """

    # ---------------------------------------------------------------------------------
    # DYNAMIC RELATION FIELDS
    # ---------------------------------------------------------------------------------

    # Initialize location-related dynamic relation fields
    region = DynamicRelationField(RegionSerializer)
    subregion = DynamicRelationField(SubregionSerializer)
    country = DynamicRelationField(CountrySerializer)
    state = DynamicRelationField(StateSerializer)
    city = DynamicRelationField(CitySerializer)
