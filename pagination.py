# -------------------------------------------------------------------------------------
# DYNAMIC REST IMPORTS
# -------------------------------------------------------------------------------------

from dynamic_rest.pagination import DynamicPageNumberPagination


# -------------------------------------------------------------------------------------
# DEFAULT PAGINATION
# -------------------------------------------------------------------------------------


class DefaultPagination(DynamicPageNumberPagination):
    """ A default pagination class for querysets """

    # ---------------------------------------------------------------------------------
    # CLASS ATTRIBUTES
    # ---------------------------------------------------------------------------------

    # Define page size attributes
    page_size = 20
    max_page_size = 100
    page_query_param = "page"
    page_size_query_param = "page_size"
