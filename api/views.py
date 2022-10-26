from django_filters import rest_framework as filters
from rest_framework import generics, viewsets
from rest_framework.exceptions import NotFound

from api.models import Company, Measurement, Sensor
from api.serializers import (CompanySerializer, MeasurementSerializer,
                             SensorRetrieveSerializer, SensorViewSetSerializer)
from api.utils.api_filters import LargeResultsSetPagination, MeasurementFilter


class CompanyViewSet(viewsets.ModelViewSet):
    """Viewset of company"""
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def get_object(self):
        try:
            return Company.objects.get(id=self.kwargs.get('pk'))
        except Company.DoesNotExist:
            raise NotFound('A Company with this id does not exist')


class SensorViewSet(viewsets.ModelViewSet):
    """Viewset of Sensor of a company"""
    queryset = Sensor.objects.all()
    serializer_class = SensorViewSetSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        more_context = {
            "company_pk": self.kwargs.get("company_pk"),
        }
        if "pk" in self.kwargs:
            more_context["pk"] = self.kwargs.get("pk")
        context.update(more_context)
        print("context", context)
        return context

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get("company_pk")
        try:
            company = Company.objects.get(id=company_id)
        except Company.DoesNotExist:
            raise NotFound('A Company with this id does not exist')
        self.queryset = self.queryset.filter(company=company)
        return self.queryset


class SensorRetrieveAPIView(generics.ListAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorRetrieveSerializer
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_fields = ('company', )

    def get_queryset(self):
        labels = self.request.GET.get("labels", None)
        if not labels:
            return self.queryset
        labels = labels.split(',')
        print(self.request.GET.get("labels", None), labels)
        return self.queryset.filter(labels__contains=labels)


class MeasurementCreateAPIView(generics.CreateAPIView):
    serializer_class = MeasurementSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            "sensor_pk": self.kwargs.get("sensor_pk"),
        })
        return context

    def get_queryset(self, *args, **kwargs):
        sensors_id = self.kwargs.get("sensor_pk")
        try:
            sensor = Sensor.objects.get(id=sensors_id)

        except Sensor.DoesNotExist:
            raise NotFound('A Sensor with this id does not exist')
        return self.queryset.filter(sensor=sensor)


class MeasurementListAPIView(generics.ListAPIView):
    serializer_class = MeasurementSerializer
    queryset = Measurement.objects.all()
    pagination_class = LargeResultsSetPagination
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = MeasurementFilter
