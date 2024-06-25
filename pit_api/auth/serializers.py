import uuid

from rest_framework import serializers

from pit_api.auth.models import Role, EmailVerification
from pit_api.common.base_serializers import BaseSerializer
from pit_api.users.models import User


class RegistrationSerializer(BaseSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password", "nickname", "role", "created_at"]

    username = serializers.CharField(max_length=16, required=True, allow_null=False, allow_blank=False)
    password = serializers.CharField(max_length=16, required=True, allow_null=False, allow_blank=False, write_only=True)
    nickname = serializers.CharField(max_length=16, required=True, allow_null=False, allow_blank=False)
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), required=True, allow_null=False)
    created_at = serializers.DateTimeField(allow_null=False)

    def create(self, validated_data):
        username = validated_data.get("username")
        password = validated_data.get("password")
        nickname = validated_data.get("nickname")
        role = validated_data.get("role")
        created_at = validated_data.get("created_at")

        user = User(username=username, nickname=nickname, role=role, created_at=created_at)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(BaseSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]

    username = serializers.CharField(max_length=16, required=True, allow_null=False, allow_blank=False)
    password = serializers.CharField(max_length=16, required=True, allow_null=False, allow_blank=False, write_only=True)


class EmailVerificationSerializer(BaseSerializer):
    class Meta:
        model = EmailVerification
        fields = ['email', 'code_token', 'verification_token']

    def create_verification_token(self):
        instance = self.instance
        for _ in range(10):  # Retry up to 10 times
            verification_token = uuid.uuid4()
            instance.verification_token = verification_token
            try:
                instance.save()
                break  # Break the loop if save is successful
            except:
                continue

        if not instance.verification_token:
            raise serializers.ValidationError("인증 토큰 생성에 실패했습니다. 다시 시도해주세요.")
        return instance.verification_token
