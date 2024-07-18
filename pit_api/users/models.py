from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, username, password, created_at, name=None, role_id=0):
        if not username or not password:
            raise ValueError("아이디 또는 비밀번호가 입력되지 않았습니다.")

        user = self.model(
            username=username,
            name=name,
            role_id=role_id,
            created_at=created_at if created_at else timezone.now()
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, created_at=None, name=None, role_id=0):
        user = self.create_user(
            username=username,
            password=password,
            created_at=created_at,
            name=name,
            role_id=role_id
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    from pit_api.auth.models import Role

    class Meta:
        db_table = "user"

    objects = UserManager()

    role = models.ForeignKey(Role, on_delete=models.PROTECT, null=False, db_column="role_id")
    username = models.CharField(max_length=16, unique=True, null=False, blank=False)
    nickname = models.CharField(max_length=12, unique=True, null=False, blank=False)
    email = models.EmailField()
    phone = models.CharField(max_length=16)
    created_at = models.DateTimeField(null=False)
    removed_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['created_at']

    def __str__(self):
        return self.username
