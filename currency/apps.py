# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ DJANGO IMPORTS                                                                     │
# └────────────────────────────────────────────────────────────────────────────────────┘

from django.apps import AppConfig


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ CURRENCY CONFIG                                                                    │
# └────────────────────────────────────────────────────────────────────────────────────┘


class CurrencyConfig(AppConfig):
    name = "beutils.currency"
    label = "beutils_currency"