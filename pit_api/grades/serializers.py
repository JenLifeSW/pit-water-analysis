from rest_framework import serializers
from .models import GradeStandard


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradeStandard
        fields = ["name", 'textColor', "backgroundColor", "minConcentration", "maxConcentration"]

    name = serializers.CharField(source="grade.name")
    textColor = serializers.CharField(source="grade.text_color")
    backgroundColor = serializers.CharField(source="grade.background_color")
    minConcentration = serializers.IntegerField(source="min_value")
    maxConcentration = serializers.IntegerField(source="max_value")
