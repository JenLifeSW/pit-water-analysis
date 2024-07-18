from django.contrib import admin

from pit_api.grades.models import Grade, GradeStandard


class GradeAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "text_color", "background_color"]
    search_fields = ["id", "name", "text_color", "background_color"]
    ordering = ["id", "name", "text_color", "background_color"]


class GradeStandardAdmin(admin.ModelAdmin):
    def target_name(self, obj):
        return obj.target

    target_name.short_description = "측정 항목 이름"
    target_name.admin_order_field = "target__name"

    def grade_name(self, obj):
        return obj.grade

    grade_name.short_description = "등급"
    grade_name.admin_order_field = "grade__name"

    list_display = ["id", "target_name", "grade_name", "min_value", "max_value"]
    search_fields = ["id", "target__name", "grade__name", "min_value", "max_value"]
    ordering = ["id", "target__name", "grade__name"]


admin.site.register(Grade, GradeAdmin)
admin.site.register(GradeStandard, GradeStandardAdmin)
