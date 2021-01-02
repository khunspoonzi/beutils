# See https://gist.github.com/martin056/65a04eb37da98d25f1c4712fb70f939f

# -------------------------------------------------------------------------------------
# GENERAL IMPORTS
# -------------------------------------------------------------------------------------

import re

# -------------------------------------------------------------------------------------
# TYPE IMPORTS
# -------------------------------------------------------------------------------------

from typing import Dict, Callable, Optional


# -------------------------------------------------------------------------------------
# CAMELIZE STRING
# -------------------------------------------------------------------------------------


def camelize_string(string: str) -> str:
    """ Transforms a snake_case string to a camelCase string """

    # Camelcase and return the input string
    return "".join(
        word.lower() if i == 0 else word.title()
        for i, word in enumerate(string.split("_"))
    )


# -------------------------------------------------------------------------------------
# SNAKEIFY STRING
# -------------------------------------------------------------------------------------


def snakeify_string(string: str) -> str:
    """ Transforms a camelCase string to a snake_case string """

    # Snake case and return the input string
    return re.sub("([A-Z])([a-z0-9]+)", r"_\1\2", string).lower()


# -------------------------------------------------------------------------------------
# CASEIFY DATA
# -------------------------------------------------------------------------------------


def caseify_data(data: Dict, caseify_func: Callable) -> Optional[Dict]:

    # Initialize caseified data
    caseified_data = {}

    # Return if data is None
    if data is None:
        return

    # ---------------------------------------------------------------------------------
    # CASE OF LIST
    # ---------------------------------------------------------------------------------

    # Check if data is a list
    if isinstance(data, list):

        # Initialize new data
        new_data = []

        # Iterate over data
        for item in data:

            # Check if item is a dict
            if isinstance(item, dict):

                # Caseify item and append to new data
                new_data.append(caseify_data(item, caseify_func))

                # Continue here
                continue

            # Append item to new data
            new_data.append(item)

        # Return new data
        return new_data

    # ---------------------------------------------------------------------------------
    # CASE OF DICT
    # ---------------------------------------------------------------------------------

    # Iterate over data
    for key, value in data.items():

        # Caseify key
        caseified_key = caseify_func(key)

        # Check if value is not a dict or list
        if not (isinstance(value, dict) or isinstance(value, list)):

            # Add to caseified data
            caseified_data[caseified_key] = value

            # Continue here
            continue

        # Check if value is a list
        if isinstance(value, list):

            # Initialize new value
            new_value = []

            # Iterate over value
            for item in value:

                # Check if item is a dict
                if isinstance(item, dict):

                    # Caseify and append to new value
                    new_value.append(caseify_data(item, caseify_func))

                    # Continue here
                    continue

                # Add item to new value
                new_value.append(item)

            # Add new value to casified data
            caseified_data[caseified_key] = new_value

        # Otherwise check if value is a dict
        elif isinstance(value, dict):

            # Add caseified value to caseified data
            caseified_data[caseified_key] = caseify_data(value, caseify_func)

    # ---------------------------------------------------------------------------------
    # RETURN CASEIFIED DATA
    # ---------------------------------------------------------------------------------

    return caseified_data


# -------------------------------------------------------------------------------------
# CAMELIZE DATA
# -------------------------------------------------------------------------------------


def camelize_data(data: dict) -> dict:
    return caseify_data(data, camelize_string)


# -------------------------------------------------------------------------------------
# SNAKEIFY DATA
# -------------------------------------------------------------------------------------


def snakeify_data(data: dict) -> dict:
    return caseify_data(data, snakeify_string)
