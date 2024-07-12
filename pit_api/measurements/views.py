from datetime import datetime

from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response

from pit_api.common.exceptions import BadRequest400Exception, NotFound404Exception
from pit_api.common.views import ManagerAPIView
from pit_api.grades.models import GradeStandard
from pit_api.grades.serializers import GradeSerializer
from pit_api.measurements.models import MeasurementTarget, MeasurementData, TankTargetAssociation
from pit_api.measurements.serializers import MeasurementTargetSerializer, MeasurementTargetDisplaySerializer, \
    MeasurementHistorySerializer
from pit_api.measurements.swaggers import schema_get_measured_data_detail_dict
from pit_api.tanks.models import Tank


class MeasurementTargetListAPIView(ManagerAPIView):
    def get(self, request):
        targets = MeasurementTarget.objects.all()
        serializer = MeasurementTargetSerializer(targets, many=True)
        return Response({"measurementTargets": serializer.data}, status=status.HTTP_200_OK)


class MeasurementHistoryAPIView(ManagerAPIView):
    @swagger_auto_schema(**schema_get_measured_data_detail_dict)
    def get(self, request, tank_id):
        target_id = request.query_params.get("target-id")
        weeks = request.query_params.get("weeks")
        start_date = request.query_params.get("start-date")
        end_date = request.query_params.get("end-date")

        if not target_id:
            raise BadRequest400Exception({"message": "측정 항목 id를 입력하세요."})
        if not weeks:
            weeks = 4

        try:
            target = MeasurementTarget.objects.get(id=target_id)
        except:
            raise NotFound404Exception({"message": "측정 항목을 찾을 수 없습니다."})
        try:
            tank = Tank.objects.get(id=tank_id)
        except:
            raise NotFound404Exception({"message": "수조 정보를 찾을 수 없습니다."})

        def ensure_aware(date_str):
            parsed_date = datetime.fromisoformat(date_str)
            if timezone.is_naive(parsed_date):
                return timezone.make_aware(parsed_date, timezone.get_current_timezone())
            return parsed_date

        if end_date:
            end_date = ensure_aware(end_date)
            if start_date:
                start_date = ensure_aware(start_date)
            else:
                start_date = end_date - timezone.timedelta(weeks=int(weeks))
        else:
            end_date = timezone.now()
            start_date = end_date - timezone.timedelta(weeks=int(weeks))

        tank_target_associations = TankTargetAssociation.objects.filter(tank=tank, target=target)
        measurement_datas = MeasurementData.objects.filter(
            tank_target__in=tank_target_associations,
            measured_at__range=(start_date, end_date)
        ).order_by("-measured_at")

        grade_standards = GradeStandard.objects.filter(target=target)

        target_serializer = MeasurementTargetDisplaySerializer(target)
        data_serializer = MeasurementHistorySerializer(measurement_datas, many=True)
        grade_serializer = GradeSerializer(grade_standards, many=True)

        response_data = {
            "target": target_serializer.data,
            "measurementDatas": data_serializer.data,
            "grades": grade_serializer.data
        }

        return Response(response_data, status=status.HTTP_200_OK)
