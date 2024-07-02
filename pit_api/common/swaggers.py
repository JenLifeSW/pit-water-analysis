from drf_yasg import openapi

responses_common = {
    204: "컨텐츠 없음",
    400: "잘못된 요청",
    401: "사용자 인증 실패",
    403: "권한 없음",
    404: "대상 없음",
    409: "중복 필드",
    500: "서버 에러",
}

parameters_authorization = [
    openapi.Parameter(
        "Authorization",
        openapi.IN_HEADER,
        description="Access token",
        type=openapi.TYPE_STRING,
        required=True
    ),
]
