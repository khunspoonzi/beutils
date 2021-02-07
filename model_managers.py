# ┌────────────────────────────────────────────────────────────────────────────────────┐
# ││ DJANGO IMPORTS                                                                     │ │
# └────────────────────────────────────────────────────────────────────────────────────┘

from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# ││ USER MANAGER MODEL                                                                 │ │
# └────────────────────────────────────────────────────────────────────────────────────┘


class UserManager(BaseUserManager):  # pragma: no cover
    """ A model manager for custom User model """

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # ││ CLASS ATTRIBUTES                                                               │ │
    # └────────────────────────────────────────────────────────────────────────────────┘

    # Enable this manager for migrations
    use_in_migrations = True

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # ││ _CREATE USER                                                                   │ │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def _create_user(self, email, password, **extra_fields):
        """ Creates and saves a User with a given email and password """

        # Require an email address
        if not email:
            raise ValueError(_("An email address is required"))

        # Normalize the email address
        email = self.normalize_email(email)

        # Define user object
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # ││ CREATE USER                                                                    │ │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def create_user(self, email, password=None, **extra_fields):
        """ Create and save a regular User with a given email and password """

        # Set is_staff and is_superuser to False
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        return self._create_user(email, password, **extra_fields)

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # ││ CREATE SUPERUSER                                                               │ │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def create_superuser(self, email, password, **extra_fields):
        """ Create and save a SuperUser with the given email and password """

        # Set is_staff and is_superuser to True
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        # Ensure that is_staff and is_superuser are True
        # Translators: A superuser is like a backend admin
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))

        # Translators: A superuser is like a backend admin
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True"))

        return self._create_user(email, password, **extra_fields)

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # ││ GET BY NATURAL KEY                                                             │ │
    # └────────────────────────────────────────────────────────────────────────────────┘

    def get_by_natural_key(self, email):
        """ Ensure that email is case insensitive when logging in """

        return self.get(email__iexact=email)
