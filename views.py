# -------------------------------------------------------------------------------------
# DJANGO IMPORTS
# -------------------------------------------------------------------------------------

from django.http import QueryDict

# -------------------------------------------------------------------------------------
# DJANGO REST FRAMEWORK IMPORTS
# -------------------------------------------------------------------------------------

from dynamic_rest.viewsets import DynamicModelViewSet

from rest_framework import filters, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.response import Response

# -------------------------------------------------------------------------------------
# PROJECT IMPORTS
# -------------------------------------------------------------------------------------

from beutils.cases import snakeify_data
from beutils.parsers import JSONSnakeCaseParser
from beutils.renderers import JSONCamelCaseRenderer
from beutils.serializers import IdListSerializer


# -------------------------------------------------------------------------------------
# CONTENT CASE VIEWSET MIXIN
# -------------------------------------------------------------------------------------


class ContentCaseViewSetMixin:

    # ---------------------------------------------------------------------------------
    # DISPATCH
    # ---------------------------------------------------------------------------------

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


# -------------------------------------------------------------------------------------
# MODEL VIEWSET
# -------------------------------------------------------------------------------------


class ModelViewSet(ContentCaseViewSetMixin, DynamicModelViewSet):
    """ A custom model viewset class """

    # ---------------------------------------------------------------------------------
    # CLASS ATTRIBUTES
    # ---------------------------------------------------------------------------------

    # Apply search filter backend
    filter_backends = DynamicModelViewSet.filter_backends + (filters.SearchFilter,)

    # ---------------------------------------------------------------------------------
    # BULK DELETE
    # ---------------------------------------------------------------------------------

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


# -------------------------------------------------------------------------------------
# OBTAIN AUTH TOKEN BASE
# -------------------------------------------------------------------------------------


class ObtainAuthTokenBase(ContentCaseViewSetMixin, ObtainAuthToken):

    # ---------------------------------------------------------------------------------
    # POST
    # ---------------------------------------------------------------------------------

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

    # ---------------------------------------------------------------------------------
    # UPDATE RESPONSE
    # ---------------------------------------------------------------------------------

    def update_response(self, response, user):

        # Return response by default
        return response
