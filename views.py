# -------------------------------------------------------------------------------------
# DJANGO IMPORTS
# -------------------------------------------------------------------------------------

from django.http import QueryDict

# -------------------------------------------------------------------------------------
# DJANGO REST FRAMEWORK IMPORTS
# -------------------------------------------------------------------------------------

from dynamic_rest.viewsets import DynamicModelViewSet

from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

# -------------------------------------------------------------------------------------
# PROJECT IMPORTS
# -------------------------------------------------------------------------------------

from beutils.cases import snakeify_data
from beutils.parsers import JSONSnakeCaseParser
from beutils.renderers import JSONCamelCaseRenderer


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

            # Initialize new query dict
            request_get = QueryDict("", mutable=True)

            # Snakeify query params
            request_get.update(snakeify_data(request.GET.dict()))

            # Ensure that query dict is immutable
            request_get._mutable = False

            # Redefine query params
            request.GET = request_get

        # Return parent dispatch method
        return super().dispatch(request, *args, **kwargs)


# -------------------------------------------------------------------------------------
# MODEL VIEWSET
# -------------------------------------------------------------------------------------


class ModelViewSet(ContentCaseViewSetMixin, DynamicModelViewSet):
    """ A custom model viewset class """


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
