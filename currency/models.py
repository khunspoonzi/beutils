# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ DJANGO IMPORTS                                                                     │
# └────────────────────────────────────────────────────────────────────────────────────┘

from django.core.exceptions import ValidationError
from django.db import models

# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ BEUTIL IMPORTS                                                                     │
# └────────────────────────────────────────────────────────────────────────────────────┘

from beutils.model_mixins import UniqueNameSlugModelMixin, TimeStampedModelMixin


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ CURRENCY                                                                           │
# └────────────────────────────────────────────────────────────────────────────────────┘


class Currency(UniqueNameSlugModelMixin, TimeStampedModelMixin):
    """ Currency Model """

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ COUNTRY FOREIGN KEY                                                            │
    # └────────────────────────────────────────────────────────────────────────────────┘

    country = models.ForeignKey(
        "beutils_location.Country",
        related_name="currencies",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ NAME PLURAL                                                                    │
    # └────────────────────────────────────────────────────────────────────────────────┘

    name_plural = models.CharField(max_length=255)

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ CODE                                                                           │
    # └────────────────────────────────────────────────────────────────────────────────┘

    code = models.CharField(max_length=10, unique=True)

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ NUMBER                                                                         │
    # └────────────────────────────────────────────────────────────────────────────────┘

    number = models.PositiveIntegerField(unique=True)

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ SYMBOLS                                                                        │
    # └────────────────────────────────────────────────────────────────────────────────┘

    symbol = models.CharField(max_length=5)

    symbol_native = models.CharField(max_length=20)

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ KIND                                                                           │
    # └────────────────────────────────────────────────────────────────────────────────┘

    # Define currency kind constants
    CRYPTO = "crypto"
    FIAT = "fiat"

    # Define currency kind choices
    KIND_CHOICES = [
        (CRYPTO, "Crypto"),
        (FIAT, "Fiat"),
    ]

    # Define kind model field
    kind = models.CharField(max_length=10, choices=KIND_CHOICES)

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ STRING METHOD                                                                  │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def __str__(self):
        """ Custom String Method """

        return self.code

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ SAVE                                                                           │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def save(self, *args, **kwargs):
        """ Custom Save Method """

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ PRE-SAVE UPDATED                                                           │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Iterate over non-null fields
        for field, display in (
            (self.name, "name"),
            (self.code, "code"),
            (self.number, "number"),
            (self.kind, "kind"),
        ):

            # Check if field is null
            if not field:

                # Raise ValidationError
                raise ValidationError(f"{display.title()} cannot be an empty string")

        # Uppercase and string code
        self.code = self.code.upper().strip()

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ SAVE OBJECT                                                                │
        # └────────────────────────────────────────────────────────────────────────────┘

        return super().save(*args, **kwargs)

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ EMOJI                                                                          │
    # └────────────────────────────────────────────────────────────────────────────────┘

    @property
    def emoji(self):
        """ Returns the emoji of the currency if applicable """

        # Check if currency is fiat
        if self.kind == Currency.FIAT:

            # Check if currency has a country
            if self.country and self.country.emoji:

                # Return country emoji
                return self.country.emoji

            # Check if currency is Euro
            if self.code == "EUR":

                # Return European Union emoji
                return "🇪🇺"

        # Return empty string by default
        return ""

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ EMOJI U                                                                        │
    # └────────────────────────────────────────────────────────────────────────────────┘

    @property
    def emoji_u(self):
        """ Returns the unicode emoji of the currency if applicable """

        # Check if currency is fiat
        if self.kind == Currency.FIAT:

            # Check if currency has a country
            if self.country and self.country.emoji_u:

                # Return country emoji
                return self.country.emoji_u

            # Check if currency is Euro
            if self.code == "EUR":

                # Return European Union emoji
                return "U+1F1EA U+1F1FA"

        # Return empty string by default
        return ""

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ META                                                                           │
    # └────────────────────────────────────────────────────────────────────────────────┘

    class Meta:

        # Define verbose names
        verbose_name = "Currency"
        verbose_name_plural = "Currencies"
