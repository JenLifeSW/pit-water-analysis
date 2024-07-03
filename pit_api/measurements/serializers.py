from rest_framework import serializers

from pit_api.common.base_serializers import BaseSerializer
from pit_api.grades.models import GradeStandard
from pit_api.measurements.models import MeasurementData, MeasurementTarget


class MeasurementTargetSerializer(BaseSerializer):
    class Meta:
        model = MeasurementTarget
        fields = ["id", "name"]


class MeasurementTargetDisplaySerializer(BaseSerializer):
    class Meta:
        model = MeasurementTarget
        fields = ["name", "unit"]

    unit = serializers.CharField(source="display_unit")


class MeasurementDataSerializer(BaseSerializer):
    class Meta:
        model = MeasurementData
        fields = ["target", "lastMeasuredAt", "value", "grade", "color"]

    target = MeasurementTargetDisplaySerializer()
    lastMeasuredAt = serializers.DateTimeField(source="measured_at", format="%Y-%m-%dT%H:%M:%S")
    value = serializers.SerializerMethodField()
    grade = serializers.SerializerMethodField()
    color = serializers.SerializerMethodField()

    def get_value(self, obj):
        target = obj.target
        value = obj.value

        return round(value * target.display_multiplier, 4)

    def _get_grade_standard(self, obj):
        grade_standard = GradeStandard.objects.filter(
            target=obj.target,
            min_value__lte=self.get_value(obj),
            max_value__gte=self.get_value(obj)
        ).first()

        return grade_standard

    def get_grade(self, obj):
        grade_standard = self._get_grade_standard(obj)

        return grade_standard.grade.name if grade_standard else "알 수 없음"

    def get_color(self, obj):
        grade_standard = self._get_grade_standard(obj)

        return grade_standard.grade.color if grade_standard else "#000000"


class MeasurementHistorySerializer(BaseSerializer):
    class Meta:
        model = MeasurementData
        fields = ["measuredAt", "value"]

    measuredAt = serializers.DateTimeField(source="measured_at", format="%Y-%m-%dT%H:%M:%S")
    value = serializers.SerializerMethodField()

    def get_value(self, obj):
        target = obj.target
        value = obj.value

        return round(value * target.display_multiplier, 4)
