# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ DJANGO IMPORTS                                                                     │
# └────────────────────────────────────────────────────────────────────────────────────┘

from django.conf import settings
from django.contrib.auth import get_user_model

# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ FACTORY BOY IMPORTS                                                                │
# └────────────────────────────────────────────────────────────────────────────────────┘

import factory

# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ PROJECT IMPORTS                                                                    │
# └────────────────────────────────────────────────────────────────────────────────────┘

from beutils.tools import slugify


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ PROJECT NAME AND SLUG                                                              │
# └────────────────────────────────────────────────────────────────────────────────────┘

# Get project name
project_name = settings.PROJECT_NAME

# Get project slug
project_slug = slugify(project_name)


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ BASE USER FACTORY                                                                  │
# └────────────────────────────────────────────────────────────────────────────────────┘


class BaseUserFactory(factory.django.DjangoModelFactory):
    """ Base User Factory """

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ FIELDS                                                                         │
    # └────────────────────────────────────────────────────────────────────────────────┘

    # Define email
    email = factory.LazyAttribute(
        lambda x: f"{x.first_name}.{x.last_name}@{project_slug}.com"
    )

    # Define first, middle, and last names
    first_name = factory.Faker("first_name")
    middle_name = factory.Faker("last_name")
    last_name = factory.Faker("last_name")

    # Set email verified to True
    email_verified = True

    # ┌────────────────────────────────────────────────────────────────────────────────┐
    # │ META                                                                           │
    # └────────────────────────────────────────────────────────────────────────────────┘

    class Meta:

        # Define model
        model = get_user_model()

        # Define get or create fields
        django_get_or_create = ("email",)
