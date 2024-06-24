from rest_framework import serializers
from .models import GradeStandard


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradeStandard
        fields = ['name', 'color', 'minConcentration', 'maxConcentration']

    name = serializers.CharField(source='grade.name')
    color = serializers.CharField(source='grade.color')
    minConcentration = serializers.IntegerField(source='min_value')
    maxConcentration = serializers.IntegerField(source='max_value')
