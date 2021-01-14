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

    # ---------------------------------------------------------------------------------
    # GET PAGE METADATA
    # ---------------------------------------------------------------------------------

    def get_page_metadata(self):
        """ Constructs the meta data for the paginated response """

        return {
            "total_results": self.page.paginator.count,
            "total_pages": self.page.paginator.num_pages,
            self.page_query_param: self.page.number,
            self.page_size_query_param: self.get_page_size(self.request),
        }
