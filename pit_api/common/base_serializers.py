from rest_framework import serializers, status
from rest_framework.response import Response


def get_error_message(errors):
    if isinstance(errors, list):
        error_object = errors[0]
    else:
        error_object = errors

    field, error = next(iter(error_object.items()))
    return {field: error[0], "code": error[0].code}


class BaseSerializer(serializers.ModelSerializer):
    def get_error_response(self):
        error_message = get_error_message(self.errors)

        return Response({"message": error_message}, status=status.HTTP_400_BAD_REQUEST)

    def get_error_body(self):
        error_message = get_error_message(self.errors)

        return {"message": error_message}
