from django.apps import AppConfig
from django.db.models.signals import post_migrate


def create_initial_datas(sender, **kwargs):
    from pit_api.auth.models import Role
    from pit_api.fish_species.models import FishSpecies
    from pit_api.measurements.models import MeasurementTarget
    from pit_api.grades.models import Grade

    if not Role.objects.exists():
        Role.objects.create(name="user", description="사용자", id=0)
        Role.objects.create(name="manager", description="매니저", id=10)
        Role.objects.create(name="admin", description="어드민", id=20)
        Role.objects.create(name="operator", description="운영자", id=30)

    if not FishSpecies.objects.exists():
        FishSpecies.objects.create(name="기타")
        FishSpecies.objects.create(name="광어")
        FishSpecies.objects.create(name="우럭")

    if not MeasurementTarget.objects.exists():
        MeasurementTarget.objects.create(name="질산성 질소", display_unit="ppm")
        MeasurementTarget.objects.create(name="온도", display_unit="˚C")

    if not Grade.objects.exists():
        Grade.objects.create(name="안전", text_color="#00D2D2", background_color="#D7F6F6")
        Grade.objects.create(name="경고", text_color="#FF6D00", background_color="#FFE5D2")
        Grade.objects.create(name="위험", text_color="#FA5A5A", background_color="#FFEAEA")


class PitApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pit_api'

    def ready(self):
        post_migrate.connect(create_initial_datas, sender=self)
