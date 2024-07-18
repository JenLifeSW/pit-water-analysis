from django.contrib import admin

from pit_api.measurements.models import MeasurementTarget, TankTargetAssociation, MeasurementData


class MeasurementTargetAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "display_unit")
    search_fields = ("id", "name", "display_unit")
    ordering = ("id", "name", "display_unit")


class TankTargetAssociationAdmin(admin.ModelAdmin):
    def tank_name(self, obj):
        return obj.tank.name

    tank_name.short_description = "수조 이름"
    tank_name.admin_order_field = "tank__name"

    def target_name(self, obj):
        return obj.target.name

    target_name.short_description = "측정 항목 이름"
    target_name.admin_order_field = "target__name"

    list_display = ("id", "tank_name", "target_name", "tank_id", "target_id")
    search_fields = ("id", "tank__name", "target__name", "tank_id", "target_id")
    ordering = ("id", "tank__name", "target__name", "tank_id", "target_id")


class MeasurementDataAdmin(admin.ModelAdmin):
    list_display = ("id", "tank_target", "value", "measured_at")
    search_fields = ("id", "tank_target", "value", "measured_at")
    ordering = ("id", "tank_target", "value", "measured_at")


admin.site.register(MeasurementTarget, MeasurementTargetAdmin)
admin.site.register(TankTargetAssociation, TankTargetAssociationAdmin)
admin.site.register(MeasurementData, MeasurementDataAdmin)
