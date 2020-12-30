# -------------------------------------------------------------------------------------
# DJANGO IMPORTS
# -------------------------------------------------------------------------------------

from django.http import QueryDict

# -------------------------------------------------------------------------------------
# DJANGO REST FRAMEWORK IMPORTS
# -------------------------------------------------------------------------------------

from dynamic_rest.viewsets import DynamicModelViewSet

# -------------------------------------------------------------------------------------
# PROJECT IMPORTS
# -------------------------------------------------------------------------------------

from beutils.cases import snakeify_data
from beutils.parsers import JSONSnakeCaseParser
from beutils.renderers import JSONCamelCaseRenderer


# -------------------------------------------------------------------------------------
# DYNAMIC MODEL VIEWSET
# -------------------------------------------------------------------------------------


class DynamicModelViewSet(DynamicModelViewSet):
    """ A custom dynamic model viewset class  """

    # ---------------------------------------------------------------------------------
    # DISPATCH
    # ---------------------------------------------------------------------------------

    def dispatch(self, request, *args, **kwargs):
        """ Custom Dispatch Method """

        # Get query params
        request_get = request.GET

        # Make query params mutable
        request_get._mutable = True

        # Check if case is specified
        _case = request.GET.pop("_case", ["snake"])[0].lower().strip()

        # Check if case is camel
        if _case == "camel":

            # Set camel case renderer class
            self.renderer_classes = (JSONCamelCaseRenderer,)

            # Set camel case parser class
            self.parser_classes = (JSONSnakeCaseParser,)

            # Initialize new query dict
            request_get = QueryDict("", mutable=True)

            # Snakeify query params
            request_get.update(snakeify_data(request_get.dict()))

        # Ensure that query dict is immutable
        request_get._mutable = False

        # Redefine query params
        request.GET = request_get

        # Return parent dispatch method
        return super().dispatch(request, *args, **kwargs)
