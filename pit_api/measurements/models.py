from django.db import models

from pit_api.tanks.models import Tank


class MeasurementTarget(models.Model):
    class Meta:
        db_table = "measurement_target"

    name = models.CharField(max_length=16, null=False, blank=False)
    display_unit = models.CharField(max_length=8, null=False, blank=False)
    display_multiplier = models.FloatField(default=1.0)


class MeasurementData(models.Model):
    class Meta:
        db_table = "measurement_data"

    tank = models.ForeignKey(Tank, on_delete=models.PROTECT)
    target = models.ForeignKey(MeasurementTarget, on_delete=models.PROTECT)
    value = models.PositiveIntegerField(null=False)
    measured_at = models.DateTimeField(auto_now_add=True)
    index = models.PositiveIntegerField(null=False)

