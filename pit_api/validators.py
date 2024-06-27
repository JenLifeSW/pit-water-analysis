from django.utils.deconstruct import deconstructible


@deconstructible
class BaseValidator:
    def __call__(self, value):
        self.validate(value)

    def validate(self, value):
        pass
