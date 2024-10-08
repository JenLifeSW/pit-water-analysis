from django.db import models
from django.utils import timezone

from pit_api.tanks.models import Tank


class MeasurementTarget(models.Model):
    def __str__(self):
        return self.name

    class Meta:
        db_table = "measurement_target"

    name = models.CharField(max_length=16, null=False, blank=False)
    display_unit = models.CharField(max_length=8, null=False, blank=False)


class TankTargetAssociation(models.Model):
    def __str__(self):
        return f"{self.tank} - {self.target}"

    class Meta:
        db_table = "tank_target_association"

    tank = models.ForeignKey(Tank, on_delete=models.PROTECT)
    target = models.ForeignKey(MeasurementTarget, on_delete=models.PROTECT)


class MeasurementData(models.Model):
    class Meta:
        db_table = "measurement_data"

    tank_target = models.ForeignKey(TankTargetAssociation, on_delete=models.PROTECT)
    value = models.FloatField(null=False)
    measured_at = models.DateTimeField()
    index = models.PositiveIntegerField(null=False)

    def save(self, *args, **kwargs):
        if not self.measured_at:
            self.measured_at = timezone.now()
        super().save(*args, **kwargs)
