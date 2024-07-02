from drf_yasg import openapi

from pit_api.common.swaggers import responses_common, parameters_authorization
from pit_api.hatcheries.serializers import HatcherySerializer
from pit_api.tanks.swaggers import properties_tank

properties_hatchery = {
    "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="양식장 ID"),
    "name": openapi.Schema(type=openapi.TYPE_STRING, description="양식장 이름"),
    "description": openapi.Schema(type=openapi.TYPE_STRING, description="양식장 설명"),
    "address": openapi.Schema(type=openapi.TYPE_STRING, description="주소"),
    "addressDetail": openapi.Schema(type=openapi.TYPE_STRING, description="상세 주소"),
}

properties_hatchery_detail = {
    **properties_hatchery,
    "tanks": openapi.Schema(
        type=openapi.TYPE_ARRAY, items=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties=properties_tank
        ),
        description="수조 정보",
    )
}

schema_hatchery_list = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "hatcheries": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties=properties_hatchery,
            )
        ),
    },
    description="양식장 리스트",
)

schema_hatchery_detail = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "hatchery": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties=properties_hatchery_detail,
            ),
        ),
    },
    description="양식장 상세 정보",
)

parameters_hatchery = parameters_authorization[:] + [
    openapi.Parameter(
        "hatchery_id",
        openapi.IN_PATH,
        description="양식장 id",
        type=openapi.TYPE_INTEGER,
        required=True
    ),
]

schema_add_hatchery_dict = {
    "operation_summary": "양식장 추가",
    "request_body": HatcherySerializer,
    "responses": {
        201: openapi.Response(
            description="양식장 추가 성공",
            schema=schema_hatchery_list
        ),
        400: responses_common[400],
        401: responses_common[401],
        403: responses_common[403],
        404: responses_common[404],
        409: responses_common[409],
        500: responses_common[500],
    },
    "manual_parameters": parameters_authorization,
}

schema_get_hatchery_list_dict = {
    "operation_summary": "양식장 리스트 조회",
    "responses": {
        200: openapi.Response(
            description="양식장 리스트 조회 성공",
            schema=schema_hatchery_list
        ),
        401: responses_common[401],
        403: responses_common[403],
        500: responses_common[500],
    },
    "manual_parameters": parameters_authorization,
}

schema_get_hatchery_info_dict = {
    "operation_summary": "양식장 상세 조회",
    "responses": {
        200: openapi.Response(
            description="양식장 상세 조회 성공",
            schema=schema_hatchery_detail
        ),
        401: responses_common[401],
        403: responses_common[403],
        404: responses_common[404],
        500: responses_common[500],
    },
    "manual_parameters": parameters_hatchery,
}

schema_update_hatchery_info_dict = {
    "operation_summary": "양식장 정보 수정",
    "request_body": HatcherySerializer,
    "responses": {
        200: openapi.Response(
            description="양식장 정보 수정 성공",
            schema=schema_hatchery_detail,
        ),
        400: responses_common[400],
        401: responses_common[401],
        403: responses_common[403],
        404: responses_common[404],
        409: responses_common[409],
        500: responses_common[500],
    },
    "manual_parameters": parameters_hatchery,
}

schema_delete_hatchery_info_dict = {
    "operation_summary": "양식장 삭제",
    "responses": {
        204: openapi.Response(
            description="양식장 삭제 성공"
        ),
        401: responses_common[401],
        403: responses_common[403],
        404: responses_common[404],
        500: responses_common[500],
    },
    "manual_parameters": parameters_hatchery,
}
