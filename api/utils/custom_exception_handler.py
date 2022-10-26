from rest_framework import exceptions
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """ a custom exception to handle 400 and 500 error"""
    if isinstance(exc, ValueError):
        exc = exceptions.ParseError(detail=exc)
    response = exception_handler(exc, context)
    if response is not None:
        response.data['status_code'] = response.status_code
    else:
        exc = exceptions.APIException(detail=exc)
        response = exception_handler(exc, context)
    return response
