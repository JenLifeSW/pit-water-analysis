from pit_api.common.base_serializers import BaseSerializer
from pit_api.fish_species.models import FishSpecies


class FishSpeciesSerializer(BaseSerializer):
    class Meta:
        models = FishSpecies
        fields = ["id", "name"]
