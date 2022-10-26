from rest_framework import serializers
from rest_framework.exceptions import NotFound

from api.models import Company, Measurement, Sensor
from api.utils.api_exceptions import MeasurementValueNotMatchFormatException


class SensorViewSetSerializer(serializers.ModelSerializer):
    """ Serializer class for SensorViewSet """

    class Meta:
        model = Sensor
        fields = ("sensorId", "company", "active", "labels")
        read_only_fields = ("company", )

    def get_object_company(self):
        if 'company_pk' in self.context:
            try:
                return Company.objects.get(id=self.context['company_pk'])
            except Company.DoesNotExist:
                raise NotFound('A Company with this id does not exist')

    def create(self, validated_data):
        company = self.get_object_company()
        validated_data['company'] = company
        return super().create(validated_data)

    def update(self, instance, validated_data):
        company = self.get_object_company()
        validated_data['company'] = company
        validated_data['sensorId'] = self.context['pk']
        return super().update(instance, validated_data)


class SensorRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sensor
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = '__all__'


class MeasurementSerializer(serializers.ModelSerializer):

    def validate(self, data):
        if "value" in data.keys():
            if "temperature" not in data['value'] or "rssi" not in data[
                    'value'] or "humidity" not in data['value']:
                raise MeasurementValueNotMatchFormatException()
        return data

    class Meta:
        model = Measurement
        fields = ("id", "sensor", "date", "value")
        read_only_fields = ("sensor", )

    def get_object_sensor(self):
        if 'sensor_pk' in self.context:
            try:
                return Sensor.objects.get(sensorId=self.context['sensor_pk'])
            except Sensor.DoesNotExist:
                raise NotFound('A Sensor with this id does not exist')

    def create(self, validated_data):
        sensor = self.get_object_sensor()
        validated_data['sensor'] = sensor
        return super().create(validated_data)
