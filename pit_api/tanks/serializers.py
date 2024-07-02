from django.db.models import Max
from rest_framework import serializers

from pit_api.common.base_serializers import BaseSerializer
from pit_api.fish_species.models import FishSpecies
from pit_api.measurements.models import MeasurementData
from pit_api.measurements.serializers import MeasurementDataSerializer
from pit_api.tanks.models import Tank
from pit_api.tanks.validators import TankNameValidator, TankDescriptionValidator


class TankSerializer(BaseSerializer):
    class Meta:
        model = Tank
        fields = ["id", "name", "fishSpeciesId", "description"]

    name = serializers.CharField(required=True, min_length=2, validators=[TankNameValidator()])
    description = serializers.CharField(required=False, validators=[TankDescriptionValidator()])
    fishSpeciesId = serializers.PrimaryKeyRelatedField(queryset=FishSpecies.objects.all(), source="fish_species")


class TankInfoSerializer(BaseSerializer):
    class Meta:
        model = Tank
        fields = ["id", "name", "description", "fishSpecies", "lastMeasuredAt"]

    fishSpecies = serializers.SerializerMethodField()
    lastMeasuredAt = serializers.SerializerMethodField()

    def get_fishSpecies(self, obj):
        fish_species = obj.fish_species
        return {
            "id": fish_species.id,
            "name": fish_species.name
        }

    def get_lastMeasuredAt(self, obj):
        latest_measurement = MeasurementData.objects.filter(tank=obj).order_by('-measured_at').first()
        return latest_measurement.measured_at if latest_measurement else None


class TankDetailSerializer(BaseSerializer):
    class Meta:
        model = Tank
        fields = ["id", "name", "description", "fishSpecies", "measurementDatas"]

    fishSpecies = serializers.SerializerMethodField()
    measurementDatas = serializers.SerializerMethodField()

    def get_fishSpecies(self, obj):
        fish_species = obj.fish_species
        return {
            "id": fish_species.id,
            "name": fish_species.name
        }

    def get_measurementDatas(self, obj):
        latest_measurements = MeasurementData.objects.filter(tank=obj).values('target').annotate(
            latest_measured_at=Max('measured_at')
        )

        latest_measurement_data = MeasurementData.objects.filter(
            tank=obj,
            measured_at__in=[measurement['latest_measured_at'] for measurement in latest_measurements]
        )

        return MeasurementDataSerializer(latest_measurement_data, many=True).data
