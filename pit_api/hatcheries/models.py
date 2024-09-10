from django.db import models
from django.utils import timezone

from pit_api.users.models import User


class HatcheryImage(models.Model):
    class Meta:
        db_table = "hatchery_image"

    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)


class Hatchery(models.Model):
    def __str__(self):
        return self.name

    class Meta:
        db_table = "hatchery"

    name = models.CharField(max_length=30, null=False, blank=False)
    description = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=50, null=True, blank=True)
    address_detail = models.CharField(max_length=50, null=True, blank=True)
    image = models.ForeignKey(HatcheryImage, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    removed_at = models.DateTimeField(null=True, blank=True)

    def delete(self, using=None, keep_parents=False):
        self.removed_at = timezone.now()
        self.save(using=using)


class HatcheryManagerAssociation(models.Model):
    class Meta:
        db_table = "hatchery_manager_association"
        unique_together = ["user", "hatchery"]

    hatchery = models.ForeignKey(Hatchery, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
