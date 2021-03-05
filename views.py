# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │DJANGO REST FRAMEWORK IMPORTS                                                       │
# └────────────────────────────────────────────────────────────────────────────────────┘

from dynamic_rest.viewsets import DynamicModelViewSet

from rest_framework import filters, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.response import Response

# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │PROJECT IMPORTS                                                                     │
# └────────────────────────────────────────────────────────────────────────────────────┘

from beutils.cases import snakeify_data
from beutils.parsers import JSONSnakeCaseParser
from beutils.renderers import JSONCamelCaseRenderer
from beutils.serializers import IdListSerializer


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │CONTENT CASE VIEWSET MIXIN                                                          │
# └────────────────────────────────────────────────────────────────────────────────────┘


class ContentCaseViewSetMixin:

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │DISPATCH                                                                        │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def dispatch(self, request, *args, **kwargs):
        """ Custom Dispatch Method """

        # Get headers
        headers = request.META

        # Get content case
        content_case = headers.get("HTTP_CONTENT_CASE", "json/snake").lower().strip()

        # Check if content case is camel
        if content_case == "json/camel":

            # Set camel case renderer class
            self.renderer_classes = (JSONCamelCaseRenderer,)

            # Set camel case parser class
            self.parser_classes = (JSONSnakeCaseParser,)

            # Redefine query params
            request.GET = snakeify_data(request.GET)

        # Return parent dispatch method
        return super().dispatch(request, *args, **kwargs)


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │MODEL VIEWSET                                                                       │
# └────────────────────────────────────────────────────────────────────────────────────┘


class ModelViewSet(ContentCaseViewSetMixin, DynamicModelViewSet):
    """ A custom model viewset class """

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │CLASS ATTRIBUTES                                                                │
    # └────────────────────────────────────────────────────────────────────────────────┘

    # Apply search filter backend
    filter_backends = DynamicModelViewSet.filter_backends + (filters.SearchFilter,)

    # Initialize bulk create options
    bulk_create_unique_fields = None
    bulk_create_update_existing = False

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │BULK CREATE                                                                     │
    # └────────────────────────────────────────────────────────────────────────────────┘

    # /api/v1/{{ model }}/bulk-create/
    @action(
        detail=False,
        methods=("post",),
        url_path="bulk-create",
    )
    def bulk_create(self, request, *args, **kwargs):

        # Get serializer class
        SerializerClass = self.get_serializer_class()

        # Get unique fields and whether to update existing
        unique_fields = self.bulk_create_unique_fields

        # Check if unique fields are specified
        if unique_fields:

            # Determine whether to update existing objects
            update_existing = self.bulk_create_update_existing

            # Create a new serializer class for the bulk update
            class SerializerClass(SerializerClass):
                """ A wrapper for the existing serializer class """

                # Init Method
                def __init__(self, *args, **kwargs):
                    """ Custom Init Method """

                    # Call super init method
                    super().__init__(*args, **kwargs)

                    # Iterate over fields
                    for field_name, field_object in self.fields.items():

                        pass

                # Meta class
                class Meta(SerializerClass.Meta):
                    """ Meta Class """

                # Create Method
                def create(self, validated_data):
                    """ Custom Create Method """

                    # Get model
                    Model = SerializerClass.Meta.model

                    # Get model dict
                    model_dict = {
                        k: validated_data.pop(k)
                        for k in unique_fields
                        if k in validated_data
                    }

                    # Check if existing objects should be updated
                    if update_existing:

                        # Update or create object
                        obj, created = Model.objects.update_or_create(
                            **model_dict, defaults=validated_data
                        )

                    # Otherwise ignore existing objects
                    else:
                        # Get or create object
                        obj, created = Model.objects.get_or_create(
                            **model_dict, defaults=validated_data
                        )

                    # Return object
                    return obj

        # Get serializer
        serializer = SerializerClass(
            data=request.data, many=True, context={"request": request}
        )

        # Validate serializer
        serializer.is_valid(raise_exception=True)

        # Save serializer
        serializer.save()

        # Return 204 response
        return Response(status=status.HTTP_201_CREATED)

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │BULK DELETE                                                                     │
    # └────────────────────────────────────────────────────────────────────────────────┘

    # /api/v1/{{ model }}/bulk-delete/
    @action(
        detail=False,
        methods=("post",),
        url_path="bulk-delete",
    )
    def bulk_delete(self, request, *args, **kwargs):

        # Get serializer
        # Dynamic mixin does not play well with non-model serializer
        # Avoid setting serializer class directly in action
        serializer = IdListSerializer(data=request.data)

        # Validate serializer
        serializer.is_valid(raise_exception=True)

        # Delete requested objects
        self.get_queryset().filter(id__in=serializer.validated_data["ids"]).delete()

        # Return 204 response
        return Response(status=status.HTTP_204_NO_CONTENT)


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ AUTH API VIEW                                                                      │
# └────────────────────────────────────────────────────────────────────────────────────┘


class AuthAPIView(ContentCaseViewSetMixin, ObtainAuthToken):

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │POST                                                                            │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def post(self, request, *args, **kwargs):

        # Get serializer
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )

        # Validate serializer
        serializer.is_valid(raise_exception=True)

        # Get user
        user = serializer.validated_data["user"]

        # Get or create token
        token, created = Token.objects.get_or_create(user=user)

        # Initialize response
        response = {"token": token.key}

        # Update response
        response = self.update_response(response, user)

        # Return response
        return Response(response)

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │UPDATE RESPONSE                                                                 │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def update_response(self, response, user):

        # Return response by default
        return response
