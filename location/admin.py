# -------------------------------------------------------------------------------------
# DJANGO IMPORTS
# -------------------------------------------------------------------------------------

from django.contrib import admin

# -------------------------------------------------------------------------------------
# PROJECT IMPORTS
# -------------------------------------------------------------------------------------

from beutils.location.models import City, Country, Region, State, Subregion


# -------------------------------------------------------------------------------------
# REGION ADMIN
# -------------------------------------------------------------------------------------


class RegionAdmin(admin.ModelAdmin):
    """ Region Admin Class """

    # ---------------------------------------------------------------------------------
    # CLASS ATTRIBUTES
    # ---------------------------------------------------------------------------------

    # Define list display
    list_display = [
        "id",
        "name",
        "created_at",
        "updated_at",
    ]

    # Define list display links
    list_display_links = ["id", "name"]

    # Define search fields
    search_fields = ["name", "slug"]


# -------------------------------------------------------------------------------------
# SUBREGION ADMIN
# -------------------------------------------------------------------------------------


class SubregionAdmin(admin.ModelAdmin):
    """ Subregion Admin Class """

    # ---------------------------------------------------------------------------------
    # CLASS ATTRIBUTES
    # ---------------------------------------------------------------------------------

    # Define list display
    list_display = [
        "id",
        "name",
        "created_at",
        "updated_at",
    ]

    # Define list display links
    list_display_links = ["id", "name"]

    # Define search fields
    search_fields = ["name", "slug"]


# -------------------------------------------------------------------------------------
# COUNTRY ADMIN
# -------------------------------------------------------------------------------------


class CountryAdmin(admin.ModelAdmin):
    """ Country Admin Class """

    # ---------------------------------------------------------------------------------
    # CLASS ATTRIBUTES
    # ---------------------------------------------------------------------------------

    # Define list display
    list_display = [
        "id",
        "name",
        "created_at",
        "updated_at",
    ]

    # Define list display links
    list_display_links = ["id", "name"]

    # Define search fields
    search_fields = ["name", "slug"]


# -------------------------------------------------------------------------------------
# STATE ADMIN
# -------------------------------------------------------------------------------------


class StateAdmin(admin.ModelAdmin):
    """ State Admin Class """

    # ---------------------------------------------------------------------------------
    # CLASS ATTRIBUTES
    # ---------------------------------------------------------------------------------

    # Define list display
    list_display = [
        "id",
        "name",
        "created_at",
        "updated_at",
    ]

    # Define list display links
    list_display_links = ["id", "name"]

    # Define search fields
    search_fields = ["name", "slug"]


# -------------------------------------------------------------------------------------
# CITY ADMIN
# -------------------------------------------------------------------------------------


class CityAdmin(admin.ModelAdmin):
    """ City Admin Class """

    # ---------------------------------------------------------------------------------
    # CLASS ATTRIBUTES
    # ---------------------------------------------------------------------------------

    # Define list display
    list_display = [
        "id",
        "name",
        "created_at",
        "updated_at",
    ]

    # Define list display links
    list_display_links = ["id", "name"]

    # Define search fields
    search_fields = ["name", "slug"]


# -------------------------------------------------------------------------------------
# ADMIN REGISTRATION
# -------------------------------------------------------------------------------------

# Register model admins
admin.site.register(Region, RegionAdmin)
admin.site.register(Subregion, SubregionAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(City, CityAdmin)
