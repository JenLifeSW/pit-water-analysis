from drf_yasg import openapi

from pit_api.common.swaggers import responses_common, parameters_authorization

schema_fish_species_list = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    description="어종 리스트",
    properties={
        "fishSpecies": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="어종 id"),
                    "name": openapi.Schema(type=openapi.TYPE_STRING, description="어종 이름")
                }
            )
        )
    },
)

schema_get_fish_species_list_dict = {
    "operation_summary": "어종 리스트 조회",
    "responses": {
        200: openapi.Response(
            description="어종 리스트 조회 성공",
            schema=schema_fish_species_list
        ),
        401: responses_common[401],
        403: responses_common[403],
        500: responses_common[500],
    },
    "manual_parameters": parameters_authorization,
}
