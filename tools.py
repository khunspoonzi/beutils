# ┌────────────────────────────────────────────────────────────────────────────────────┐
# GENERAL IMPORTS
# └────────────────────────────────────────────────────────────────────────────────────┘

import json

from unidecode import unidecode


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# READ JSON
# └────────────────────────────────────────────────────────────────────────────────────┘


def read_json(path):
    """ Returns a JSON object from a file path """

    # Read JSON file
    try:
        with open(path) as f:
            json_object = json.load(f)

        # Return JSON object
        return json_object

    # Return None if file not found
    except FileNotFoundError:
        return None


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# SLUGIFY
# └────────────────────────────────────────────────────────────────────────────────────┘


def slugify(string, decode=True):
    """ Returns a slugified version of a string input """

    # Return empty string if no text value passed
    if not string:
        return ""

    # Remove special characters
    if decode:
        string = unidecode(string)

    # Lowercase and strip slug
    string = string.lower().strip()

    # Return slugified string
    return string
