# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ DJANGO IMPORTS                                                                     │
# └────────────────────────────────────────────────────────────────────────────────────┘

from django.db import models

# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ PROJECT IMPORTS                                                                    │
# └────────────────────────────────────────────────────────────────────────────────────┘

from beutils.tools import slugify


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ DESCRIPTION MODEL MIXIN                                                            │
# └────────────────────────────────────────────────────────────────────────────────────┘


class DescriptionModelMixin(models.Model):
    """ Base model for models with a description """

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ DESCRIPTION                                                                    │
    # └────────────────────────────────────────────────────────────────────────────────┘

    description = models.TextField(blank=True)

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ META                                                                           │
    # └────────────────────────────────────────────────────────────────────────────────┘

    class Meta:

        # Set abstract to True
        abstract = True


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ EMOJI MODEL MIXIN                                                                  │
# └────────────────────────────────────────────────────────────────────────────────────┘


class EmojiModelMixin(models.Model):
    """ Base model for models with an emoji field """

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ EMOJI                                                                          │
    # └────────────────────────────────────────────────────────────────────────────────┘

    emoji = models.CharField(max_length=5, blank=True)
    emoji_u = models.CharField(max_length=20, blank=True)

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ META                                                                           │
    # └────────────────────────────────────────────────────────────────────────────────┘

    class Meta:

        # Set abstract to True
        abstract = True


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ FULL NAME MODEL MIXIN                                                              │
# └────────────────────────────────────────────────────────────────────────────────────┘


class FullNameModelMixin(models.Model):
    """ Base model for models with first, middle, and last name fields """

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ NAME FIELDS                                                                    │
    # └────────────────────────────────────────────────────────────────────────────────┘

    first_name = models.CharField(max_length=50)

    middle_name = models.CharField(max_length=50, blank=True)

    last_name = models.CharField(max_length=50, blank=True)

    has_eastern_name = models.BooleanField(blank=True, default=False)

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ STRING METHOD                                                                  │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def __str__(self):
        """ Custom String Method """

        return self.full_name

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ SAVE                                                                           │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def save(self, *args, **kwargs):
        """ Custom Save Method """

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ PRE-SAVE UPDATED                                                           │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Strip names
        self.first_name = self.first_name.strip()
        self.middle_name = self.middle_name.strip()
        self.last_name = self.last_name.strip()

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ SAVE OBJECT                                                                │
        # └────────────────────────────────────────────────────────────────────────────┘

        return super().save(*args, **kwargs)

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ FULL NAME                                                                      │
    # └────────────────────────────────────────────────────────────────────────────────┘

    @property
    def full_name(self):
        """ Returns full name of a user """

        # Get first name as a required field
        full_name = self.first_name

        # Get middle name and append to full name
        middle_name = self.middle_name
        if middle_name:
            full_name = f"{full_name} {middle_name}"

        # Get last name and append to full name
        last_name = self.last_name
        if last_name:
            full_name = (
                f"{last_name}, {full_name}"
                if self.has_eastern_name
                else f"{full_name} {last_name}"
            )

        # Return concatenated full name
        return full_name

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ META                                                                           │
    # └────────────────────────────────────────────────────────────────────────────────┘

    class Meta:

        # Set abstract to True
        abstract = True


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ NAME SLUG MODEL MIXIN                                                              │
# └────────────────────────────────────────────────────────────────────────────────────┘


class NameSlugModelMixin(models.Model):
    """ Base model for models with a name and slug Field """

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ NAME AND SLUG                                                                  │
    # └────────────────────────────────────────────────────────────────────────────────┘

    name = models.CharField(max_length=255, verbose_name="name")
    slug = models.CharField(max_length=255, blank=True, verbose_name="slug")

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ STRING METHOD                                                                  │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def __str__(self):
        """ Custom String Method """

        return self.name

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ SAVE                                                                           │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def save(self, *args, **kwargs):
        """ Custom Save Method """

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ PRE-SAVE UPDATED                                                           │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Create slug from name field
        self.slug = slugify(self.name)

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ SAVE OBJECT                                                                │
        # └────────────────────────────────────────────────────────────────────────────┘

        return super().save(*args, **kwargs)

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ META                                                                           │
    # └────────────────────────────────────────────────────────────────────────────────┘

    class Meta:

        # Set abstract to True
        abstract = True


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ ORIGIN ID MODEL MIXIN                                                              │
# └────────────────────────────────────────────────────────────────────────────────────┘


class OriginIdModelMixin(models.Model):
    """ Base model for models with an origin ID field """

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ ORIGIN ID                                                                      │
    # └────────────────────────────────────────────────────────────────────────────────┘

    origin_id = models.CharField(max_length=255, blank=True)

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ META                                                                           │
    # └────────────────────────────────────────────────────────────────────────────────┘

    class Meta:

        # Set abstract to True
        abstract = True


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ TELEGRAM USER MODEL MIXIN                                                          │
# └────────────────────────────────────────────────────────────────────────────────────┘


class TelegramUserModelMixin(models.Model):
    """ Base model for models with Telegram-related fields """

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ TELEGRAM CREDENTIALS                                                           │
    # └────────────────────────────────────────────────────────────────────────────────┘

    telegram_user_id = models.PositiveIntegerField(unique=True, blank=True, null=True)
    telegram_chat_id = models.PositiveIntegerField(unique=True, blank=True, null=True)

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ META                                                                           │
    # └────────────────────────────────────────────────────────────────────────────────┘

    class Meta:

        # Set abstract to True
        abstract = True


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ TIME STAMPED MODEL MIXIN                                                           │
# └────────────────────────────────────────────────────────────────────────────────────┘


class TimeStampedModelMixin(models.Model):
    """ Base model for models with a created_at and updated_at timestamp """

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ CREATED AT AND UPDATED AT                                                      │
    # └────────────────────────────────────────────────────────────────────────────────┘

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="updated at")

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ META                                                                           │
    # └────────────────────────────────────────────────────────────────────────────────┘

    class Meta:

        # Set abstract to True
        abstract = True


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ UNIQUE NAME SLUG MODEL MIXIN                                                       │
# └────────────────────────────────────────────────────────────────────────────────────┘


class UniqueNameSlugModelMixin(NameSlugModelMixin):
    """ Base model for models with unique name and slug field """

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ NAME AND SLUG                                                                  │
    # └────────────────────────────────────────────────────────────────────────────────┘

    name = models.CharField(max_length=255, unique=True, verbose_name="name")
    slug = models.CharField(
        max_length=255, unique=True, blank=True, verbose_name="slug"
    )

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ META                                                                           │
    # └────────────────────────────────────────────────────────────────────────────────┘

    class Meta:

        # Set abstract to True
        abstract = True
