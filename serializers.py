# ------------------------------------------------------------------------------------
# DJANGO REST FRAMEWORK IMPORTS
# ------------------------------------------------------------------------------------

from dynamic_rest.serializers import DynamicModelSerializer
from rest_framework.serializers import IntegerField, ListField, Serializer


# -------------------------------------------------------------------------------------
# ID LIST SERIALIZER
# -------------------------------------------------------------------------------------


class IdListSerializer(Serializer):
    """ A serializer class for a general list of object IDs """

    ids = ListField(child=IntegerField())


# -------------------------------------------------------------------------------------
# MODEL SERIALIZER
# -------------------------------------------------------------------------------------


class ModelSerializer(DynamicModelSerializer):
    """ A custom model serializer class """
