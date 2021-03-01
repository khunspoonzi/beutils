# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ GENERAL IMPORTS                                                                    │
# └────────────────────────────────────────────────────────────────────────────────────┘

import requests


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ BASE ADAPTER                                                                       │
# └────────────────────────────────────────────────────────────────────────────────────┘


class BaseAdapter:
    """ A base adapter """

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ CLASS ATTRIBUTES                                                               │
    # └────────────────────────────────────────────────────────────────────────────────┘

    # Initialize base URL
    base_url = ""

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ ENTER METHOD                                                                   │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def __enter__(self):
        """ Enter Method """
        return self

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ EXIT METHOD                                                                    │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def __exit__(self, *args, **kwargs):
        """ Exit Method """

        # Close the adapter
        self.close()

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │GET_DEFAULT_HEADERS                                                             │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def get_default_headers(self):
        """ Returns a dictionary of default headers for API requests """

        # Return an empty dict
        return {}

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │REQUEST                                                                         │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def request(self, endpoint, headers=None, params=None, post_data=None):
        """ Makes an HTTP request to an API endpoint """

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ CONSTRUCT URL                                                              │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Construct URL
        url = self.base_url.rstrip("/") + "/" + endpoint.strip("/")

        # Check if params is not null
        if params:

            # Check if params is a dict
            if type(params) is dict:

                # Construct params
                params = "&".join([f"{k}={v}" for k, v in params.items()])

            # Add params to URL
            url = url + "?" + params

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ GET HEADERS                                                                │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Get default headers
        _headers = self.get_default_headers()

        # Check if headers were supplied
        if type(headers) is dict:

            # Update final headers
            _headers.update(headers)

        # Set headers
        headers = _headers

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ MAKE REQUEST                                                               │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Initialize request dict
        request_dict = {
            "url": url,
            "headers": headers,
        }

        # Check if request is POST
        if post_data:

            # Add POST data to request dict
            request_dict["data"] = post_data

            # Make POST request
            response = requests.post(**request_dict)

        # Otherwise GET by default
        else:

            # Make GET request
            response = requests.get(**request_dict)

        # Return response JSON and status code
        return response.json(), response.status_code

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ _VALIDATE                                                                      │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def _validate(self, label, items, interface):
        """ Validates a set of items based on an interface """

        # Check if items is a dict
        if type(items) is dict:

            # Convert dict to list
            items = items.values()

        # Iterate over items
        for item in items:

            # Iterate over item interface
            for key, info in interface.items():

                # Get value info
                value_type = info["type"]
                value_type = value_type if type(value_type) is list else [value_type]
                value_required = info.get("required", True)
                value_validator = info.get("validator")

                # Ensure None is handled correctly
                value_type = [type(t) if t is None else t for t in value_type]

                # Check if key not in item
                if key not in item:

                    # Raise exception
                    raise Exception(f"{label} missing {key} of type {value_type}")

                # Get value
                value = item[key]

                # Check if value is missing
                if value_required and not value and value is not False:

                    # Raise exception
                    raise Exception(f"{label} value for {key} cannot be nullish")

                # Check if value is missing or not the correct type
                if type(value) not in value_type:

                    # Raise exception
                    raise Exception(f"{label} {key} is not of type {value_type}")

                # Check if custom validator is defined
                if value_validator and not value_validator(value):

                    # Raise exception
                    raise Exception(f"{label} {key} is not valid: {value}")

        # Return items
        return items

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ CLOSE                                                                          │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def close(self):
        """ Performs any additional logic necessary to close the adapter """
        return
