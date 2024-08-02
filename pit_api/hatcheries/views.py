from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from pit_api.common.exceptions import BadRequest400Exception, NotFound404Exception, Conflict409Exception
from pit_api.common.permissions import IsAdminRole
from pit_api.common.views import AdminAPIView, ManagerAPIView
from pit_api.hatcheries.models import Hatchery, HatcheryManagerAssociation
from pit_api.hatcheries.serializers import HatcherySerializer, HatcheryDetailSerializer
from pit_api.hatcheries.swaggers import schema_get_hatchery_list_dict, schema_add_hatchery_dict, \
    schema_get_hatchery_info_dict, schema_update_hatchery_info_dict, schema_delete_hatchery_info_dict


class HatcheryAPIView(AdminAPIView):
    @swagger_auto_schema(**schema_add_hatchery_dict)
    @transaction.atomic
    def post(self, request):
        user = request.user
        name = request.data.get("name")

        if not name:
            raise BadRequest400Exception({"message": "양식장 이름을 입력하세요."})
        existing_hatchery = Hatchery.objects.filter(hatcherymanagerassociation__user=user, name=name).exists()

        if existing_hatchery:
            raise Conflict409Exception({"message": "이미 사용중인 양식장 이름입니다."})

        serializer = HatcherySerializer(data=request.data)
        if not serializer.is_valid():
            return serializer.get_error_response()
        hatchery = serializer.save()

        HatcheryManagerAssociation.objects.create(hatchery=hatchery, user=user)

        hatcheries = Hatchery.objects.filter(hatcherymanagerassociation__user=user)
        hatcheries_serializer = HatcherySerializer(hatcheries, many=True)

        return Response({"hatcheries": hatcheries_serializer.data}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(**schema_get_hatchery_list_dict)
    def get(self, request):
        user = request.user
        hatcheries = Hatchery.objects.filter(hatcherymanagerassociation__user=user, removed_at__isnull=True)
        serializer = HatcherySerializer(hatcheries, many=True)

        return Response({"hatcheries": serializer.data}, status=status.HTTP_200_OK)


class HatcheryInfoAPIView(ManagerAPIView):
    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() == 'delete':
            self.permission_classes = [IsAdminRole]
        return super().dispatch(request, *args, **kwargs)

    def get_hatchery(self, hatchery_id, user):
        try:
            hatchery = Hatchery.objects.get(id=hatchery_id)
        except:
            raise NotFound404Exception({"message": "양식장 정보를 찾을 수 없습니다."})

        if user.role.id != 30 and not HatcheryManagerAssociation.objects.filter(hatchery=hatchery, user=user).exists():
            raise PermissionDenied({"message": "이 양식장에 접근할 권한이 없습니다."})

        if hatchery.removed_at:
            raise BadRequest400Exception({"message": "삭제된 양식장입니다."})
        return hatchery

    @swagger_auto_schema(**schema_update_hatchery_info_dict)
    @transaction.atomic
    def patch(self, request, hatchery_id):
        user = request.user
        name = request.data.get("name")
        hatchery = self.get_hatchery(hatchery_id, user)

        if name:
            existing_hatchery = Hatchery.objects.filter(hatcherymanagerassociation__user=user, name=name).exists()

            if existing_hatchery and name != hatchery.name:
                raise Conflict409Exception({"message": "이미 사용중인 양식장 이름입니다."})

        serializer = HatcherySerializer(hatchery, data=request.data, partial=True)
        if not serializer.is_valid():
            return serializer.get_error_response()

        serializer.save()
        detail_serializer = HatcheryDetailSerializer(hatchery)
        return Response({"hatchery": detail_serializer.data}, status=status.HTTP_200_OK)

    @swagger_auto_schema(**schema_get_hatchery_info_dict)
    def get(self, request, hatchery_id):
        user = request.user
        hatchery = self.get_hatchery(hatchery_id, user)

        serializer = HatcheryDetailSerializer(hatchery)

        return Response({"hatchery": serializer.data}, status=status.HTTP_200_OK)

    @swagger_auto_schema(**schema_delete_hatchery_info_dict)
    def delete(self, request, hatchery_id):
        user = request.user
        hatchery = self.get_hatchery(hatchery_id, user)
        hatchery.delete()

        hatcheries = Hatchery.objects.filter(hatcherymanagerassociation__user=user, removed_at__isnull=True)
        serializer = HatcherySerializer(hatcheries, many=True)

        return Response({"hatcheries": serializer.data}, status=status.HTTP_200_OK)
