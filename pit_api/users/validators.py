import re

from django.core.exceptions import ValidationError

from pit_api.validators import BaseValidator


class UsernameValidator(BaseValidator):
    def validate(self, value):
        if len(value) < 2:
            raise ValidationError("아이디의 길이는 2자 이상이어야 합니다.")
        if len(value) > 12:
            raise ValidationError("아이디의 길이는 16자를 초과할 수 없습니다.")
        if not re.search(r"^[a-zA-Z0-9]+$", value):
            raise ValidationError("아이디는 영문 대소문자와 숫자만 사용가능합니다.")


class PasswordValidator(BaseValidator):
    def validate(self, value):
        if len(value) < 6:
            raise ValidationError("비밀번호의 길이는 6자 이상이어야 합니다.")
        if len(value) > 16:
            raise ValidationError("비밀번호의 길이는 16자를 초과할 수 없습니다.")
        if not re.search(r"[a-zA-Z]", value):
            raise ValidationError("비밀번호는 영문자를 포함해야 합니다.")
        if not re.search(r"\d", value):
            raise ValidationError("비밀번호는 숫자를 포함해야 합니다.")
        if not re.search(r"^[a-zA-Z\d!@#$%^*+=\-]+$", value):
            raise ValidationError("'!@#$%^*+=-' 외의 특수문자는 사용할 수 없습니다.")


class NicknameValidator(BaseValidator):
    def validate(self, value):
        if len(value) < 2:
            raise ValidationError("닉네임의 길이는 2자 이상이어야 합니다.")
        if len(value) > 12:
            raise ValidationError("닉네임의 길이는 12자를 초과할 수 없습니다.")
        if not re.search(r"^[a-zA-Z0-9가-힣]+$", value):
            raise ValidationError("닉네임은 한글 또는 영문, 숫자만 사용 가능합니다.")


class EmailValidator(BaseValidator):
    def validate(self, value):
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", value):
            raise ValidationError("올바른 메일 형식이 아닙니다.")


class PhoneNumberValidator(BaseValidator):
    def validate(self, value):
        if not re.match(r"^[0-9-]{11,16}$", value):
            raise ValidationError("올바른 번호 형식이 아닙니다.")
