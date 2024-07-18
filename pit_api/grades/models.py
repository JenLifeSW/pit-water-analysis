from django.db import models

from pit_api.measurements.models import MeasurementTarget


class Grade(models.Model):
    class Meta:
        db_table = "grade"

    name = models.CharField(max_length=16, null=False)
    text_color = models.CharField(max_length=7, null=False, default="#FF0000")
    background_color = models.CharField(max_length=7, null=False, default="#000000")


class GradeStandard(models.Model):
    class Meta:
        db_table = "grade_standard"

    target = models.ForeignKey(MeasurementTarget, on_delete=models.CASCADE)
    grade = models.ForeignKey(Grade, on_delete=models.PROTECT)
    min_value = models.FloatField(null=True, default=0)
    max_value = models.FloatField(null=True, default=999999)
