from django.db import transaction
from rest_framework import status
from rest_framework.response import Response

from pit_api.common.exceptions import NotFound404Exception, Conflict409Exception, BadRequest400Exception
from pit_api.common.views import ManagerAPIView
from pit_api.fish_species.models import FishSpecies
from pit_api.tanks.models import Tank
from pit_api.tanks.serializers import TankSerializer, TankDetailSerializer


class TankInfoAPIView(ManagerAPIView):
    def get_tank(self, tank_id):
        try:
            tank = Tank.objects.get(id=tank_id)
        except:
            raise NotFound404Exception({"message": "수조 정보를 찾을 수 없습니다."})

        if tank.removed_at:
            raise BadRequest400Exception({"message": "삭제된 수조입니다."})
        return tank

    @transaction.atomic
    def patch(self, request, tank_id):
        tank = self.get_tank(tank_id)
        name = request.data.get("name")
        hatchery = tank.hatchery

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

    def get(self, request, tank_id):
        tank = self.get_tank(tank_id)
        serializer = TankDetailSerializer(tank)

        return Response({"tank": serializer.data}, status=status.HTTP_200_OK)

    def delete(self, request, tank_id):
        tank = self.get_tank(tank_id)
        tank.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
