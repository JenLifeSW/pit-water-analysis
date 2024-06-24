from django.urls import path, include

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="PIT",
        default_version='1.0.0',
        description="PIT 기반 수질 분석 서비스 API 명세",
        # terms_of_service="https://www.google.com/policies/terms/",
        # contact=openapi.Contact(email="이메일"),  # 부가정보
        # license=openapi.License(name="mit"),  # 부가정보
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # path('/swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('/swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('/redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc-v1'),

    path("/auth", include("pit_api.auth.urls")),
    path("/hatcheries", include("pit_api.hatcheries.urls")),
    path("/tanks", include("pit_api.tanks.urls")),
    path("/users", include("pit_api.users.urls")),
]
