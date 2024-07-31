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


class MeasurementTargetListAPIView(ManagerAPIView):
    def get(self, request):
        targets = MeasurementTarget.objects.all()
        serializer = MeasurementTargetSerializer(targets, many=True)
        return Response({"measurementTargets": serializer.data}, status=status.HTTP_200_OK)


class MeasurementHistoryAPIView(ManagerAPIView):
    @swagger_auto_schema(**schema_get_measured_data_detail_dict)
    def get(self, request, tank_id):
        user = request.user
        target_id = request.query_params.get("target-id")
        duration = request.query_params.get("duration")
        start_date = request.query_params.get("start-date")
        end_date = request.query_params.get("end-date")

        if not target_id:
            raise BadRequest400Exception({"message": "측정 항목 id를 입력하세요."})

        try:
            target = MeasurementTarget.objects.get(id=target_id)
        except:
            raise NotFound404Exception({"message": "측정 항목을 찾을 수 없습니다."})

        def ensure_aware(date_str):
            parsed_date = datetime.fromisoformat(date_str)
            if timezone.is_naive(parsed_date):
                return timezone.make_aware(parsed_date, timezone.get_current_timezone())
            return parsed_date

        def transform_measured_at(start_date, end_date):
            def re_format(obj):
                if obj.year == datetime.now().year:
                    return obj.strftime("%m.%d")
                return obj.strftime("%Y.%m.%d")

            start_date_str = re_format(start_date)
            end_date_str = re_format(end_date)
            if start_date_str == end_date_str:
                return start_date_str
            return f"{start_date_str}-{end_date_str}"

        def adjust_to_midnight(dt):
            if dt.hour < 12:
                return dt.replace(hour=0, minute=0, second=0, microsecond=0)
            else:
                return (dt + timezone.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)

        if duration and (duration == "1mon" or duration == "3mon" or duration == "1y"):
            end_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
            if duration == "1mon":
                start_date = end_date - timezone.timedelta(days=30)
            elif duration == "3mon":
                start_date = end_date - timezone.timedelta(days=90)
            elif duration == "1y":
                start_date = end_date - timezone.timedelta(days=365)

        else:
            if end_date:
                end_date = ensure_aware(end_date)
                if start_date:
                    start_date = ensure_aware(start_date)
                else:
                    start_date = end_date - timezone.timedelta(days=30)
            else:
                end_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
                start_date = end_date - timezone.timedelta(days=30)

        end_date = end_date + timezone.timedelta(days=1)

        from pit_api.tanks.views import TankInfoAPIView
        tank, _ = TankInfoAPIView().get_tank(tank_id, user)

        tank_target_associations = TankTargetAssociation.objects.filter(tank=tank, target=target)

        last_measured_data = MeasurementData.objects.filter(
            tank_target__in=tank_target_associations
        ).order_by("-measured_at").first()

        grade_standards = GradeStandard.objects.filter(target=target)
        if grade_standards:
            min_value_grade_standard = grade_standards.order_by('min_value').first().min_value
        else:
            min_value_grade_standard = 0
        measurement_datas = []

        total_duration = end_date - start_date
        total_days = total_duration.days
        if total_days <= 30:
            delta_days = 1
        else:
            delta_days = total_days / 30.0

        delta_seconds = delta_days * 24 * 60 * 60
        delta = timezone.timedelta(seconds=delta_seconds)

        start_date_aware = ensure_aware(start_date.isoformat())
        end_date_aware = ensure_aware(end_date.isoformat())
        ref_date = start_date_aware

        set_len = total_days if total_days <= 30 else 30
        set_interval = (total_duration - timezone.timedelta(1)) / (set_len - 1)
        dates = [adjust_to_midnight(start_date + i * set_interval) for i in range(set_len)]
        n = 0
        while adjust_to_midnight(ref_date) < end_date_aware:
            group_start_date = adjust_to_midnight(ref_date)
            group_end_date = adjust_to_midnight(ref_date + delta) - timezone.timedelta(microseconds=1)

            group_measurement = MeasurementData.objects.filter(
                tank_target__in=tank_target_associations,
                measured_at__range=(group_start_date, group_end_date)
            ).order_by('-value').first()

            measured_at_str = transform_measured_at(group_start_date, group_end_date)
            if group_measurement is not None:
                value = group_measurement.value
            else:
                value = min_value_grade_standard
            measurement_datas.append({"measuredAt": dates[n], "value": value, "detail": measured_at_str})

            ref_date = ref_date + delta
            n += 1

        grade_standards = GradeStandard.objects.filter(target=target)

        target_serializer = MeasurementTargetDisplaySerializer(target)
        last_measured_data_serializer = MeasurementHistorySerializer(last_measured_data)
        grade_serializer = GradeSerializer(grade_standards, many=True)

        response_data = {
            "target": target_serializer.data,
            "lastMeasurementData": last_measured_data_serializer.data,
            "measurementDatas": measurement_datas,
            "grades": grade_serializer.data
        }

        return Response(response_data, status=status.HTTP_200_OK)
