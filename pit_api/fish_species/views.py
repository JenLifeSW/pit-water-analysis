from rest_framework import status
from rest_framework.response import Response

from pit_api.common.views import ManagerAPIView
from pit_api.fish_species.models import FishSpecies
from pit_api.fish_species.serializers import FishSpeciesSerializer


class FishSpeciesAPIView(ManagerAPIView):
    def get(self, request):
        fish_species = FishSpecies.objects.all()
        serializer = FishSpeciesSerializer(fish_species, many=True)

        return Response({"fishSpecies": serializer.data}, status=status.HTTP_200_OK)
