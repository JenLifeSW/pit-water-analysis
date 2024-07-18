from django.db import models


class FishSpecies(models.Model):
    def __str__(self):
        return self.name

    class Meta:
        db_table = "fish_species"

    name = models.CharField(max_length=12, null=False, blank=False)
