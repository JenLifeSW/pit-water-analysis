from drf_yasg import openapi

from pit_api.common.swaggers import responses_common, parameters_authorization

properties_measurement_target = {
    "name": openapi.Schema(type=openapi.TYPE_STRING, description="타겟 이름"),
    "unit": openapi.Schema(type=openapi.TYPE_STRING, description="타겟 단위"),
}

properties_measured_data = {
    "measuredAt": openapi.Schema(type=openapi.TYPE_STRING, description="측정 시간"),
    "value": openapi.Schema(type=openapi.TYPE_INTEGER, description="측정 값"),
}

properties_grades = {
    "name": openapi.Schema(type=openapi.TYPE_STRING, description="등급 이름"),
    "color": openapi.Schema(type=openapi.TYPE_STRING, description="등급 색상"),
    "minValue": openapi.Schema(type=openapi.TYPE_INTEGER, description="등급 최소 값"),
    "maxValue": openapi.Schema(type=openapi.TYPE_INTEGER, description="등급 최대 값"),
}

schema_measured_data_detail = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "target": openapi.Schema(type=openapi.TYPE_OBJECT, description="측정 타겟"),
        "measurementDatas": openapi.Schema(
            type=openapi.TYPE_ARRAY, items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties=properties_measured_data,
            )
        ),
        "grades": openapi.Schema(
            type=openapi.TYPE_ARRAY, items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties=properties_grades,
            )
        ),
    }
)

parameters_measured_data_detail = parameters_authorization[:] + [
    openapi.Parameter(
        "target-id",
        openapi.IN_QUERY,
        description="타겟 id",
        type=openapi.TYPE_INTEGER,
        required=True
    ),
    openapi.Parameter(
        "weeks",
        openapi.IN_QUERY,
        description="검색할 기간",
        type=openapi.TYPE_INTEGER,
        required=False
    ),
    openapi.Parameter(
        "start-date",
        openapi.IN_QUERY,
        description="검색 시작 날짜",
        type=openapi.TYPE_INTEGER,
        required=False
    ),
    openapi.Parameter(
        "end-date",
        openapi.IN_QUERY,
        description="검색 마지막 날짜",
        type=openapi.TYPE_INTEGER,
        required=False
    ),
    openapi.Parameter(
        "tank_id",
        openapi.IN_PATH,
        description="수조 id",
        type=openapi.TYPE_INTEGER,
        required=True
    ),
]

schema_get_measured_data_detail_dict = {
    "operation_summary": "측정 항목 히스토리 조회",
    "responses": {
        200: openapi.Response(
            description="양식장 리스트 조회 성공",
            schema=schema_measured_data_detail,
        ),
        401: responses_common[401],
        403: responses_common[403],
        500: responses_common[500],
    },
    "manual_parameters": parameters_measured_data_detail,
}
