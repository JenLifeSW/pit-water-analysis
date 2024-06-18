from django.apps import AppConfig
from django.db.models.signals import post_migrate


def create_initial_roles(sender, **kwargs):
    from pit_api.auth.models import Role
    if not Role.objects.exists():
        Role.objects.create(name="user", id=0)
        Role.objects.create(name="manager", id=10)
        Role.objects.create(name="admin", id=20)
        Role.objects.create(name="operator", id=30)


class PitApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pit_api'

    def ready(self):
        post_migrate.connect(create_initial_roles, sender=self)
