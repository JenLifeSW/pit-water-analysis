import random
import string
import uuid

from django.db import models


class Role(models.Model):
    class Meta:
        db_table = "role"

    id = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=10, null=False, blank=False)


def generate_verification_code():
    while True:
        return "".join(random.choices(string.digits, k=6))


class EmailVerification(models.Model):
    from pit_api.users.models import User

    class Meta:
        db_table = "email_verification"

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, db_column="user_id")
    email = models.EmailField()
    code = models.CharField(max_length=6, default=generate_verification_code, editable=False, unique=True)
    code_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    verification_token = models.UUIDField(null=True, blank=True, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.email} - {self.code}"
