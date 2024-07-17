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
        fields = ["id", "name", "unit"]

    unit = serializers.CharField(source="display_unit")


class MeasurementDataSerializer(BaseSerializer):
    class Meta:
        model = MeasurementData
        fields = ["target", "lastMeasuredAt", "value", "grade", "textColor", "backgroundColor"]

    target = MeasurementTargetDisplaySerializer(source="tank_target.target")
    lastMeasuredAt = serializers.DateTimeField(source="measured_at", format="%Y-%m-%dT%H:%M:%S", required=False)
    value = serializers.SerializerMethodField()
    grade = serializers.SerializerMethodField()
    textColor = serializers.SerializerMethodField()
    backgroundColor = serializers.SerializerMethodField()

    def get_value(self, obj):
        if obj.value is not None:
            target = obj.tank_target.target
            value = obj.value
            return round(value * target.display_multiplier, 4)
        return None

    def _get_grade_standard(self, obj):
        if obj.value is not None:
            target = obj.tank_target.target
            grade_standard = GradeStandard.objects.filter(
                target=target,
                min_value__lte=self.get_value(obj),
                max_value__gte=self.get_value(obj)
            ).first()
            return grade_standard
        return None

    def get_grade(self, obj):
        grade_standard = self._get_grade_standard(obj)
        return grade_standard.grade.name if grade_standard else None

    def get_textColor(self, obj):
        grade_standard = self._get_grade_standard(obj)
        return grade_standard.grade.text_color if grade_standard else None

    def get_backgroundColor(self, obj):
        grade_standard = self._get_grade_standard(obj)
        return grade_standard.grade.background_color if grade_standard else None


class MeasurementHistorySerializer(BaseSerializer):
    class Meta:
        model = MeasurementData
        fields = ["measuredAt", "value"]

    measuredAt = serializers.DateTimeField(source="measured_at", format="%Y-%m-%dT%H:%M:%S")
    value = serializers.SerializerMethodField()

    def get_value(self, obj):
        target = obj.tank_target.target
        value = obj.value

        return round(value * target.display_multiplier, 4)


class LastMeasuredDataSerializer(serializers.Serializer):
    def to_representation(self, instance):
        last_measured_data = instance.get("last_measured_data")
        target = instance.get("target")

        if last_measured_data:
            last_measured_value = round(last_measured_data.value * target.display_multiplier, 4)
            last_measured_at = last_measured_data.measured_at.strftime("%Y-%m-%dT%H:%M:%S")
        else:
            last_measured_value = None
            last_measured_at = None

        return {
            "lastMeasuredAt": last_measured_at,
            "lastMeasuredValue": last_measured_value
        }
