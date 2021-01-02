# -------------------------------------------------------------------------------------
# DJANGO IMPORTS
# -------------------------------------------------------------------------------------

from django.db import models

# -------------------------------------------------------------------------------------
# PROJECT IMPORTS
# -------------------------------------------------------------------------------------

from beutils.tools import slugify


# -------------------------------------------------------------------------------------
# CUSTOM EMAIL FIELD
# -------------------------------------------------------------------------------------


class CustomEmailField(models.EmailField):
    """ A custom email field to ensure slugified emails """

    def get_prep_value(self, value):
        """ Alters the field value before validation occurs """

        # Get field value
        value = super().get_prep_value(value)

        # Check if value is not None
        if value is not None:

            # Slugify value
            value = slugify(value)

        # Return value
        return value
