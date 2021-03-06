# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │DJANGO IMPORTS                                                                      │
# └────────────────────────────────────────────────────────────────────────────────────┘

from django.apps import AppConfig


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │LOCATION CONFIG                                                                     │
# └────────────────────────────────────────────────────────────────────────────────────┘


class LocationConfig(AppConfig):
    name = "beutils.location"
    label = "beutils_location"
