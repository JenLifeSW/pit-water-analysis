from pit_api.common.base_serializers import BaseSerializer
from pit_api.fish_species.models import FishSpecies


class FishSpeciesSerializer(BaseSerializer):
    class Meta:
        model = FishSpecies
        fields = ["id", "name"]
