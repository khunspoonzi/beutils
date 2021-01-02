# ------------------------------------------------------------------------------------
# DJANGO REST FRAMEWORK IMPORTS
# ------------------------------------------------------------------------------------

from dynamic_rest.serializers import DynamicModelSerializer


# -------------------------------------------------------------------------------------
# MODEL SERIALIZER
# -------------------------------------------------------------------------------------


class ModelSerializer(DynamicModelSerializer):
    """ A custom model serializer class """
