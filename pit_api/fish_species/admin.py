from django.contrib import admin

from pit_api.fish_species.models import FishSpecies


class FishSpeciesAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["id", "name"]
    ordering = ["id", "name"]


admin.site.register(FishSpecies, FishSpeciesAdmin)
