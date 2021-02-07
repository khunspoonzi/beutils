# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │DJANGO REST FRAMEWORK IMPORTS │
# └────────────────────────────────────────────────────────────────────────────────────┘

from drf_multiple_model.pagination import MultipleModelLimitOffsetPagination
from dynamic_rest.pagination import DynamicPageNumberPagination


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │CONSTANTS │
# └────────────────────────────────────────────────────────────────────────────────────┘

RESULT_COUNT = "result_count"

# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │DEFAULT PAGINATION │
# └────────────────────────────────────────────────────────────────────────────────────┘


class DefaultPagination(DynamicPageNumberPagination):
    """ A default pagination class for querysets """

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │CLASS ATTRIBUTES │
    # └────────────────────────────────────────────────────────────────────────────────┘

    # Define page size attributes
    page_size = 20
    max_page_size = 100
    page_query_param = "page"
    page_size_query_param = "page_size"

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │GET PAGE METADATA │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def get_page_metadata(self):
        """ Constructs the meta data for the paginated response """

        return {
            self.page_query_param: self.page.number,
            self.page_size_query_param: self.get_page_size(self.request),
            "page_count": self.page.paginator.num_pages,
            RESULT_COUNT: self.page.paginator.count,
        }


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │DEFAULT MULTIPLE MODEL PAGINATION │
# └────────────────────────────────────────────────────────────────────────────────────┘


class DefaultMultipleModelPagination(MultipleModelLimitOffsetPagination):
    """ A default pagination for multiple model viewsets """

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │CLASS ATTRIBUTES │
    # └────────────────────────────────────────────────────────────────────────────────┘

    default_limit = 10

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │FORMAT RESPONSE │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def format_response(self, data):
        """
        Overrides the default response to conform to Dynamic Rest structure
        """

        # Set count (copied from source)
        self.count = self.max_count

        # Return newly structured response
        return {**data, "meta": {RESULT_COUNT: self.total}}

        return OrderedDict(
            [
                ("highest_count", self.max_count),
                ("overall_total", self.total),
                ("next", self.get_next_link()),
                ("previous", self.get_previous_link()),
                ("results", data),
            ]
        )
