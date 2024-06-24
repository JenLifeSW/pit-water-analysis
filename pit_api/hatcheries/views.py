from django.db import transaction
from rest_framework import status
from rest_framework.response import Response

from pit_api.common.exceptions import BadRequest400Exception, NotFound404Exception, Conflict409Exception
from pit_api.common.views import AdminAPIView, ManagerAPIView
from pit_api.fish_species.models import FishSpecies
from pit_api.hatcheries.models import Hatchery, HatcheryManagerAssociation
from pit_api.hatcheries.serializers import HatcherySerializer, HatcheryDetailSerializer
from pit_api.tanks.models import Tank
from pit_api.tanks.serializers import TankSerializer, TankInfoSerializer


class HatcheryAPIView(AdminAPIView):
    @transaction.atomic
    def post(self, request):
        user = request.user
        name = request.data.get("name")
        existing_hatchery = Hatchery.objects.filter(hatcherymanagerassociation__user=user, name=name).exists()

        if existing_hatchery:
            raise BadRequest400Exception({"message": "이미 사용중인 양식장 이름입니다."})

        serializer = HatcherySerializer(data=request.data)
        if not serializer.is_valid():
            return serializer.get_error_response()
        hatchery = serializer.save()

        HatcheryManagerAssociation.objects.create(hatchery=hatchery, user=user)

        hatcheries = Hatchery.objects.filter(hatcherymanagerassociation__user=user)
        hatcheries_serializer = HatcherySerializer(hatcheries, many=True)

        return Response({"hatcheries": hatcheries_serializer.data}, status=status.HTTP_201_CREATED)

    def get(self, request):
        user = request.user
        hatcheries = Hatchery.objects.filter(hatcherymanagerassociation__user=user)
        serializer = HatcherySerializer(hatcheries, many=True)

        return Response({"hatcheries": serializer.data}, status=status.HTTP_200_OK)


class HatcheryInfoAPIView(AdminAPIView):
    def get_hatchery(self, hatchery_id):
        try:
            hatchery = Hatchery.objects.get(id=hatchery_id)
        except:
            raise NotFound404Exception({"message": "양식장 정보를 찾을 수 없습니다."})

        if hatchery.removed_at:
            raise BadRequest400Exception({"message": "삭제된 양식장입니다."})
        return hatchery

    @transaction.atomic
    def patch(self, request, hatchery_id):
        hatchery = self.get_hatchery(hatchery_id)
        user = request.user
        name = request.data.get("name")

        if name:
            existing_hatchery = Hatchery.objects.filter(hatcherymanagerassociation__user=user, name=name).exists()

            if existing_hatchery and name != hatchery.name:
                raise Conflict409Exception({"message": "이미 사용중인 양식장 이름입니다."})

        serializer = HatcherySerializer(hatchery, data=request.data, partial=True)
        if not serializer.is_valid():
            return serializer.get_error_response()

        serializer.save()
        return Response({"hatchery": serializer.data}, status=status.HTTP_200_OK)

    def get(self, request, hatchery_id):
        hatchery = self.get_hatchery(hatchery_id)

        serializer = HatcheryDetailSerializer(hatchery)

        return Response({"hatchery": serializer.data}, status=status.HTTP_200_OK)

    def delete(self, request, hatchery_id):
        hatchery = self.get_hatchery(hatchery_id)
        hatchery.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class AddTankAPIView(ManagerAPIView):
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

        if name:
            if Tank.objects.filter(hatchery=hatchery, name=name).exists():
                raise Conflict409Exception({"message": "이미 사용중인 수조 이름입니다."})

        serializer = TankSerializer(data=request.data)
        if not serializer.is_valid():
            return serializer.get_error_response()

        serializer.save(hatchery=hatchery, fish_species=fish_species)

        tanks = Tank.objects.filter(hatchery=hatchery)
        tanks_serializer = TankInfoSerializer(tanks, many=True)

        return Response({"tanks": tanks_serializer.data}, status=status.HTTP_201_CREATED)
