from drf_yasg import openapi

from pit_api.common.swaggers import parameters_authorization, responses_common
from pit_api.measurements.swaggers import properties_measurement_target
from pit_api.tanks.serializers import TankSerializer

properties_measurement_data = {
    "target": openapi.Schema(
        type=openapi.TYPE_ARRAY, items=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties=properties_measurement_target
        ),
        description="측정 타겟",
    ),
    "lastMeasuredAt": openapi.Schema(type=openapi.TYPE_STRING, description="마지막 측정 시간"),
    "value": openapi.Schema(type=openapi.TYPE_INTEGER, description="측정 값"),
    "grade": openapi.Schema(type=openapi.TYPE_STRING, description="등급"),
    "color": openapi.Schema(type=openapi.TYPE_STRING, description="등급 색상"),
}

properties_fish_species = {
    "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="어종 id"),
    "name": openapi.Schema(type=openapi.TYPE_STRING, description="어종 이름"),
}

properties_tank = {
    "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="수조 id"),
    "name": openapi.Schema(type=openapi.TYPE_STRING, description="수조 이름"),
    "description": openapi.Schema(type=openapi.TYPE_STRING, description="수조 설명"),
    "fishSpecies": openapi.Schema(
        type=openapi.TYPE_ARRAY, items=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties=properties_fish_species
        ),
        description="어종",
    ),
    "lastMeasuredAt": openapi.Schema(type=openapi.TYPE_STRING, description="마지막 측정 시간"),
}

properties_tank_detail = {
    **properties_tank,
    "measurementDatas": openapi.Schema(
        type=openapi.TYPE_ARRAY, items=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties=properties_measurement_data,
        ),
        description="측정 데이터",
    )
}
properties_tank_detail.pop("lastMeasuredAt")

schema_tank_list = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "tanks": openapi.Schema(
            type=openapi.TYPE_ARRAY, items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties=properties_tank,
            )
        ),
    },
)

schema_tank_detail = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "tank": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties=properties_tank_detail,
        ),
    },
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

parameters_tank = parameters_authorization[:] + [
    openapi.Parameter(
        "tank_id",
        openapi.IN_PATH,
        description="수조 id",
        type=openapi.TYPE_INTEGER,
        required=True
    ),
]

schema_add_tank_dict = {
    "operation_summary": "수조 추가",
    "responses": {
        201: openapi.Response(
            description="수조 추가 성공",
            schema=schema_tank_list,
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

schema_get_tank_info_dict = {
    "operation_summary": "수조 상세 조회",
    "responses": {
        200: openapi.Response(
            description="수조 상세 조회 성공",
            schema=schema_tank_detail,
        ),
        401: responses_common[401],
        403: responses_common[403],
        404: responses_common[404],
        500: responses_common[500],
    },
    "manual_parameters": parameters_tank,
}

schema_update_tank_info_dict = {
    "operation_summary": "수조 정보 수정",
    "request_body": TankSerializer,
    "responses": {
        200: openapi.Response(
            description="양식장 정보 수정 성공",
            schema=schema_tank_detail,
        ),
        400: responses_common[400],
        401: responses_common[401],
        403: responses_common[403],
        404: responses_common[404],
        409: responses_common[409],
        500: responses_common[500],
    },
    "manual_parameters": parameters_tank,
}

schema_delete_tank_info_dict = {
    "operation_summary": "수조 삭제",
    "responses": {
        204: openapi.Response(
            description="수조 삭제 성공"
        ),
        401: responses_common[401],
        403: responses_common[403],
        404: responses_common[404],
        500: responses_common[500],
    },
    "manual_parameters": parameters_tank,
}
