# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ GENERAL IMPORTS                                                                    │
# └────────────────────────────────────────────────────────────────────────────────────┘

import json
import pytz

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

    # Initialize all choices
    all_choices = []

    # Iterate over choice groups
    for choice_group in choice_groups:

        # Iterate over choice group indices
        for i in range(len(choice_group)):

            # Get choice without display
            choice = choice_group[i][0]

            # Remove display from choice
            choice_group[i] = choice

            # Check if choice not in all choices
            if choice not in all_choices:

                # Append choice to all choices
                all_choices.append(choice)

    # Return all choices
    return all_choices


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ SLUGIFY                                                                            │
# └────────────────────────────────────────────────────────────────────────────────────┘


def slugify(string, decode=True, space=None):
    """ Returns a slugified version of a string input """

    # Return empty string if no text value passed
    if not string:
        return ""

    # Remove special characters
    if decode:
        string = unidecode(string)

    # Lowercase and strip slug
    string = string.lower().strip()

    # Check if space is a string
    if type(space) is str:

        # Replace spaces with the specified character
        string = string.replace(" ", space)

    # Return slugified string
    return string


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ TO UTC                                                                             │
# └────────────────────────────────────────────────────────────────────────────────────┘


def to_utc(dt):
    """ Converts a datetime object to UTC """

    # Return if datetime is null
    if not dt:
        return dt

    # Get UTC
    UTC = pytz.UTC

    # Get tzinfo
    tzinfo = dt.tzinfo

    # Return datetime if already UTC
    if tzinfo == UTC:
        return dt

    # Check if datetime is naive
    if not tzinfo:

        # Return datetime localized to UTC
        return UTC.localize(dt)

    # Otherwise convert an already timezone aware datetime to UTC
    return dt.astimezone(UTC)
