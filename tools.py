# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ GENERAL IMPORTS                                                                    │
# └────────────────────────────────────────────────────────────────────────────────────┘

import json

from unidecode import unidecode


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ IS TZ AWARE                                                                        │
# └────────────────────────────────────────────────────────────────────────────────────┘


def is_tz_aware(datetime):
    """ Determined if a datetime object is timezone aware """

    return (
        datetime.tzinfo is not None and datetime.tzinfo.utcoffset(datetime) is not None
    )


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ READ JSON                                                                          │
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
# │ REDUCE CHOICE GROUPS                                                               │
# └────────────────────────────────────────────────────────────────────────────────────┘


def reduce_choice_groups(*choice_groups):
    """
    Reduces choice groups from a list of tuples to a list of strings in place

    e.g.
        [[("waiting", "Waiting"), ("active", "Active")], [("inactive", "Inactive")]]
        [["waiting", "active"], ["inactive"]]

    Used for filtering of choice fields
    """

    # Iterate over choice groups
    for choice_group in choice_groups:

        # Iterate over choice group indices
        for i in range(len(choice_group)):

            # Remove display from choice
            choice_group[i] = choice_group[i][0]


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ SLUGIFY                                                                            │
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
