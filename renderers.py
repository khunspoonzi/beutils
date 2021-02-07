# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │DJANGO REST FRAMEWORK IMPORTS                                                       │
# └────────────────────────────────────────────────────────────────────────────────────┘

from rest_framework import renderers

# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │PROJECT IMPORTS                                                                     │
# └────────────────────────────────────────────────────────────────────────────────────┘

from beutils.cases import camelize_data

# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │JSON CAMEL CASE RENDERER                                                            │
# └────────────────────────────────────────────────────────────────────────────────────┘


class JSONCamelCaseRenderer(renderers.JSONRenderer):
    """ JSON Camel Case Renderer """

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │RENDER                                                                          │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def render(self, data, *args, **kwargs):

        # Camelize data
        camelized_data = camelize_data(data)

        # Return camelized data
        return super().render(camelized_data, *args, **kwargs)
