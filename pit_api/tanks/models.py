from django.db import models
from django.utils import timezone

from pit_api.fish_species.models import FishSpecies
from pit_api.hatcheries.models import Hatchery


class Tank(models.Model):
    class Meta:
        db_table = "tank"

    hatchery = models.ForeignKey(Hatchery, on_delete=models.PROTECT, related_name='tanks')
    fish_species = models.ForeignKey(FishSpecies, on_delete=models.PROTECT, related_name="tank")
    name = models.CharField(max_length=16, null=False, blank=False)
    description = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    species_changed_at = models.DateTimeField(auto_now_add=True)
    removed_at = models.DateTimeField(null=True)

    def delete(self, using=None, keep_parents=False):
        self.removed_at = timezone.now()
        self.save(using=using)
