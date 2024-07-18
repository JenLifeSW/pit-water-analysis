from django.contrib import admin

from pit_api.tanks.models import Tank


class TankAdmin(admin.ModelAdmin):
    def hatchery_name(self, obj):
        return obj.hatchery.name

    hatchery_name.short_description = 'Hatchery Name'
    hatchery_name.admin_order_field = "hatchery__name"

    def fish_species_name(self, obj):
        return obj.fish_species.name

    fish_species_name.short_description = 'Fish Species Name'
    fish_species_name.admin_order_field = "fish_species__name"

    list_display = (
        'id', 'name', 'hatchery_name', 'description', 'fish_species_name',
        'created_at', 'species_changed_at', 'removed_at'
    )
    search_fields = ("id", 'name', 'hatchery__name', 'fish_species__name')
    ordering = ('id', 'name', "hatchery__name", "fish_species__name", 'created_at')


admin.site.register(Tank, TankAdmin)
