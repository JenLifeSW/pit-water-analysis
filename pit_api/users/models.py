from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, username, password, created_at, name=None, role_id=0):
        if not username or not password:
            raise ValueError("아이디 또는 비밀번호가 입력되지 않았습니다.")

        user = self.model(
            username=username,
            name=name,
            role=role_id,
            created_at=created_at
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    from pit_api.auth.models import Role

    class Meta:
        db_table = "user"

    objects = UserManager()

    role = models.ForeignKey(Role, on_delete=models.PROTECT, null=False, db_column="role_id")
    username = models.CharField(max_length=16, unique=True, null=False, blank=False)
    nickname = models.CharField(max_length=16, default="사용자", null=False, blank=False)
    email = models.EmailField()
    phone = models.CharField(max_length=16)
    created_at = models.DateTimeField(null=False)
    removed_at = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'username'
