from django.contrib import admin

from pit_api.hatcheries.models import Hatchery, HatcheryManagerAssociation


class HatcheryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "address", "address_detail", "image", "created_at", "removed_at")
    search_fields = ("id", "name", "description", "address", "address_detail", "created_at", "removed_at")
    ordering = ("id", "name", "description", "address", "address_detail", "created_at", "removed_at")


class HatcheryManagerAssociationAdmin(admin.ModelAdmin):
    def hatchery_name(self, obj):
        return obj.hatchery.name

    hatchery_name.short_description = "양식장 이름"
    hatchery_name.admin_order_field = "hatchery__name"

    def user_name(self, obj):
        return obj.user.nickname

    user_name.short_description = "관리자 닉네임"
    user_name.admin_order_field = "user__nickname"

    list_display = ("id", "hatchery_name", "user_name", "hatchery_id", "user_id")
    search_fields = ("hatchery__name", "user__nickname")
    ordering = ("id", "hatchery__name", "user__nickname")

admin.site.register(Hatchery, HatcheryAdmin)
admin.site.register(HatcheryManagerAssociation, HatcheryManagerAssociationAdmin)
