from rest_framework import status
from rest_framework.exceptions import APIException


class BaseCustomException(APIException):
    detail = None
    status_code = None

    def __init__(self, detail, code):
        super().__init__(detail, code)
        self.detail = detail
        self.status_code = code


class MeasurementValueNotMatchFormatException(BaseCustomException):

    def __init__(self):
        detail = "Value entered does not match Format "
        super().__init__(detail, status.HTTP_400_BAD_REQUEST)


class SensorNotUpdateSensorIdException(BaseCustomException):

    def __init__(self):
        detail = "You can't update a sensorId"
        super().__init__(detail, status.HTTP_400_BAD_REQUEST)
