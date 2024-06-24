from django.db import models


class FishSpecies(models.Model):
    class Meta:
        db_table = "fish_species"

    name = models.CharField(max_length=12, null=False, blank=False)
