from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import PermissionDenied, APIException
from rest_framework.response import Response

from pit_api.common.exceptions import NotFound404Exception, Conflict409Exception, BadRequest400Exception
from pit_api.common.views import ManagerAPIView
from pit_api.fish_species.models import FishSpecies
from pit_api.hatcheries.models import HatcheryManagerAssociation, Hatchery
from pit_api.measurements.models import MeasurementTarget, TankTargetAssociation
from pit_api.tanks.models import Tank
from pit_api.tanks.serializers import TankSerializer, TankDetailSerializer, TankInfoSerializer
from pit_api.tanks.swaggers import schema_add_tank_dict, schema_get_tank_info_dict, schema_update_tank_info_dict, \
    schema_delete_tank_info_dict


class AddTankAPIView(ManagerAPIView):
    @swagger_auto_schema(**schema_add_tank_dict)
    @transaction.atomic
    def post(self, request, hatchery_id):
        name = request.data.get("name")
        if not name:
            raise BadRequest400Exception({"message": "수조 이름을 입력하세요."})

        try:
            hatchery = Hatchery.objects.get(id=hatchery_id)
        except:
            raise NotFound404Exception({"message": "양식장 정보를 찾을 수 없습니다."})

        try:
            fish_species = FishSpecies.objects.get(id=request.data.get("fishSpeciesId"))
        except:
            raise NotFound404Exception({"message": "어종 정보를 찾을 수 없습니다."})

        if Tank.objects.filter(hatchery=hatchery, name=name).exists():
            raise Conflict409Exception({"message": "이미 사용중인 수조 이름입니다."})

        serializer = TankSerializer(data=request.data)
        if not serializer.is_valid():
            return serializer.get_error_response()

        tank = serializer.save(hatchery=hatchery, fish_species=fish_species)
        target_ids = [1, 2, 3, 4]
        for target_id in target_ids:
            try:
                target = MeasurementTarget.objects.get(id=target_id)
            except:
                raise APIException({"message": "수조를 추가하지 못했습니다. 관리자에게 문의하세요."})

            TankTargetAssociation.objects.create(tank=tank, target=target)

        tanks = Tank.objects.filter(hatchery=hatchery)
        tanks_serializer = TankInfoSerializer(tanks, many=True)

        return Response({"tanks": tanks_serializer.data}, status=status.HTTP_201_CREATED)


class TankInfoAPIView(ManagerAPIView):
    def get_tank(self, tank_id, user):
        try:
            tank = Tank.objects.get(id=tank_id)
        except:
            raise NotFound404Exception({"message": "수조 정보를 찾을 수 없습니다."})

        hatchery = tank.hatchery
        if user.role.id != 30 and not HatcheryManagerAssociation.objects.filter(hatchery=hatchery, user=user).exists():
            raise PermissionDenied({"message": "이 수조에 접근할 권한이 없습니다."})

        if tank.removed_at:
            raise BadRequest400Exception({"message": "삭제된 수조입니다."})
        return tank, hatchery

    @swagger_auto_schema(**schema_update_tank_info_dict)
    @transaction.atomic
    def patch(self, request, tank_id):
        user = request.user
        name = request.data.get("name")
        tank, hatchery = self.get_tank(tank_id, user)

        if name:
            existing_tank = Tank.objects.filter(hatchery=hatchery, name=name).exists()
            if existing_tank and name != tank.name:
                raise Conflict409Exception({"message": "이미 사용중인 수조 이름입니다."})

        fish_species_id = request.data.get("fishSpeciesId")
        if fish_species_id is not None:
            try:
                fish_species = FishSpecies.objects.get(id=fish_species_id)
            except:
                raise NotFound404Exception({"message": "어종 정보를 찾을 수 없습니다."})

        serializer = TankSerializer(tank, data=request.data, partial=True)
        if not serializer.is_valid():
            return serializer.get_error_response()

        serializer.save()

        detail_serializer = TankDetailSerializer(tank)

        return Response({"tank": detail_serializer.data}, status=status.HTTP_200_OK)

    @swagger_auto_schema(**schema_get_tank_info_dict)
    def get(self, request, tank_id):
        user = request.user
        tank, _ = self.get_tank(tank_id, user)
        serializer = TankDetailSerializer(tank)

        return Response({"tank": serializer.data}, status=status.HTTP_200_OK)

    @swagger_auto_schema(**schema_delete_tank_info_dict)
    def delete(self, request, tank_id):
        user = request.user
        tank, _ = self.get_tank(tank_id, user)
        tank.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
