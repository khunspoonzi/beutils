# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ DJANGO IMPORTS                                                                     │
# └────────────────────────────────────────────────────────────────────────────────────┘

from django.contrib.auth.models import AbstractUser
from django.db import models

# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ BEUTIL IMPORTS                                                                     │
# └────────────────────────────────────────────────────────────────────────────────────┘

from beutils.model_fields import CustomEmailField
from beutils.model_managers import UserManager
from beutils.model_mixins import FullNameModelMixin, TimeStampedModelMixin
from beutils.tools import slugify


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ BASE USER MODEL                                                                    │
# └────────────────────────────────────────────────────────────────────────────────────┘


class BaseUser(AbstractUser, FullNameModelMixin, TimeStampedModelMixin):
    """ Custom Base User Model """

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ UNUSED FIELDS                                                                  │
    # └────────────────────────────────────────────────────────────────────────────────┘

    username = None

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ EMAIL                                                                          │
    # └────────────────────────────────────────────────────────────────────────────────┘

    USERNAME_FIELD = "email"

    email = CustomEmailField(unique=True)
    email_verified = models.BooleanField(default=False)

    REQUIRED_FIELDS = []  # Removes email from REQUIRED_FIELDS

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ META                                                                           │
    # └────────────────────────────────────────────────────────────────────────────────┘

    class Meta:

        # Set abstract to True
        abstract = True

        # Define verbose names
        verbose_name = "User"
        verbose_name_plural = "Users"

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ MODEL MANAGER                                                                  │
    # └────────────────────────────────────────────────────────────────────────────────┘

    # Use the model manager
    objects = UserManager()

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ STRING METHOD                                                                  │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def __str__(self):
        """ Custom String Method """

        # Return full name if not null, otherwise email
        return self.full_name or self.email

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ SAVE                                                                           │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def save(self, *args, **kwargs):
        """ Custom Save Method """

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ PRE-SAvE UPDATED                                                           │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Slugify and set email
        self.email = slugify(self.email)

        # Strip and set name attributes
        self.first_name = self.first_name.strip()
        self.middle_name = self.middle_name.strip()
        self.last_name = self.last_name.strip()

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ PRE-SAVE CREATED                                                           │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Determine if object is being created
        created = self._state.adding

        # Check if object has been created
        if created:

            # Check if user is superuser
            if self.is_superuser:

                # Ensure that user is active and that email is verified
                self.is_active = self.email_verified = True

            # Otherwise handle case of normal user
            else:

                # Ensure that user is inactive on creation
                self.is_active = self.email_verified = False

            # Check if first name is null
            if not self.first_name:

                # Extract email username
                email_username = self.email.split("@")[0]

                # Set first name to email username
                self.first_name = email_username

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ SAVE OBJECT                                                                │
        # └────────────────────────────────────────────────────────────────────────────┘

        # Save object
        super().save(*args, **kwargs)

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ POST-SAVE UPDATED                                                          │
        # └────────────────────────────────────────────────────────────────────────────┘

        # ┌────────────────────────────────────────────────────────────────────────────┐
        # │ POST-SAVE CREATED                                                          │
        # └────────────────────────────────────────────────────────────────────────────┘

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ DISPLAY NAME                                                                   │
    # └────────────────────────────────────────────────────────────────────────────────┘

    @property
    def display_name(self):
        """ Returns display name of a user """

        # Get first name as a required field
        display_name = self.first_name

        # Get last name and append first letter to display name
        last_name = self.last_name
        if last_name:
            display_name = f"{display_name} {last_name[0].upper()}."

        # Return concatenated display name
        return display_name
