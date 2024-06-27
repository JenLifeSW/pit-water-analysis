from django.core.exceptions import ValidationError
import re

from pit_api.validators import BaseValidator


class TankNameValidator(BaseValidator):
    def validate(self, value):
        if len(value) < 2:
            raise ValidationError("수조 이름의 길이는 2자 이상이어야 합니다.")
        if len(value) > 16:
            raise ValidationError("수조 이름의 길이는 16자를 초과할 수 없습니다.")
        if not re.search(r"^[a-zA-Z0-9가-힣]*$", value):
            raise ValidationError("수조 이름에 특수문자를 사용할 수 없습니다.")


class TankDescriptionValidator(BaseValidator):
    def validate(self, value):
        if len(value) > 255:
            raise ValidationError("수조 설명의 길이는 255자를 초과할 수 없습니다.")
        if not re.search(r"^[a-zA-Z0-9가-힣!@#$%^&*()_+\-=\[\]{};':\"\\\|,.<>?`~]*$", value):
            raise ValidationError("수조 설명에 사용할 수 없는 기호가 포함되어 있습니다.")
