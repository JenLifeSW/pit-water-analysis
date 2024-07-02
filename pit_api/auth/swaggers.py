from drf_yasg import openapi

from pit_api.auth.serializers import LoginSerializer
from pit_api.common.swaggers import responses_common

parameters_refresh = [
    openapi.Parameter(
        "Authorization",
        openapi.IN_HEADER,
        description="Refresh token",
        type=openapi.TYPE_STRING,
        required=True
    ),
]

responses_login = {
    204: openapi.Response(
        description="로그인 성공",
        headers={
            'Authorization': {
                'description': 'Bearer {refreshToken/accessToken}',
                'type': 'string',
            }
        },
    ),
    401: responses_common[401],
    500: responses_common[500],
}

responses_refresh = {
    204: openapi.Response(
        description="토큰 갱신 성공",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'access_token': openapi.Schema(type=openapi.TYPE_STRING,
                                               description="access_token"),
                'access_exp': openapi.Schema(type=openapi.TYPE_STRING,
                                             description="access_exp"),
                'refresh_token': openapi.Schema(type=openapi.TYPE_STRING,
                                                description="refresh_token"),
            }
        ),
        headers={
            'Authorization': {
                'description': 'Bearer {refreshToken/accessToken}',
                'type': 'string',
            }
        },
    ),
    401: responses_common[401],
    500: responses_common[500],
}

schema_login_dict = {
    "operation_summary": "로그인",
    "request_body": LoginSerializer,
    "responses": responses_login
}

schema_refresh_dict = {
    "operation_summary": "토큰 갱신",
    "responses": responses_login,
    "manual_parameters": parameters_refresh
}
