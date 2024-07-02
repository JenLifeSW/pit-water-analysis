from drf_yasg import openapi

from pit_api.auth.serializers import LoginSerializer
from pit_api.common.swaggers import responses_common

schema_login = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="유저 id"),
        "nickname": openapi.Schema(type=openapi.TYPE_STRING, description=" 닉네임"),
        "email": openapi.Schema(type=openapi.TYPE_STRING, description="이메일"),
        "phone": openapi.Schema(type=openapi.TYPE_STRING, description="휴대폰 번호"),
        "role": openapi.Schema(type=openapi.TYPE_STRING, description="유저 역할"),
        "hatcheryIds": openapi.Schema(
            type=openapi.TYPE_ARRAY, items=openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description="양식장 id 리스트"
            )
        ),
    },
)

parameters_refresh = [
    openapi.Parameter(
        "Authorization",
        openapi.IN_HEADER,
        description="Refresh token",
        type=openapi.TYPE_STRING,
        required=True
    ),
]

schema_login_dict = {
    "operation_summary": "로그인",
    "request_body": LoginSerializer,
    "responses": {
        200: openapi.Response(
            description="로그인 성공",
            schema=schema_login,
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
}

schema_refresh_dict = {
    "operation_summary": "토큰 갱신",
    "responses": {
        204: openapi.Response(
            description="토큰 갱신 성공",
            headers={
                'Authorization': {
                    'description': 'Bearer {accessToken}',
                    'type': 'string',
                }
            },
        ),
        401: responses_common[401],
        500: responses_common[500],
    },
    "manual_parameters": parameters_refresh
}
