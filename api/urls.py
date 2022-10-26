"""assistme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from unicodedata import name
from django.urls import include, re_path
from rest_framework import routers as re
from rest_framework import status
from rest_framework_nested import routers

from api.views import (CompanyViewSet, MeasurementCreateAPIView,
                       MeasurementListAPIView, SensorRetrieveAPIView,
                       SensorViewSet)

app_name = 'api'
router = re.DefaultRouter()
router.register(r'companies', CompanyViewSet, basename='companies')
company_router = routers.NestedSimpleRouter(router,
                                            r'companies',
                                            lookup='company')
company_router.register(r'sensors', SensorViewSet, basename='sensors')
urlpatterns = [
    re_path(r'^api/v1/', include(router.urls), name='companies'),
    re_path(r'^api/v1/', include(company_router.urls), name='sensors'),
    re_path(r'^api/v1/sensors/search/?$',
            SensorRetrieveAPIView.as_view(),
            name='sensor-search'),
    re_path(r'^api/v1/sensors/(?P<sensor_pk>[a-z0-9]+)/measurements/?$',
            MeasurementCreateAPIView.as_view(),
            name='sensor-measurements'),
    re_path(r'^api/v1/measurements/search/?$',
            MeasurementListAPIView.as_view()),
]

handler404 = 'api.urls.custom_404_view'
handler500 = 'api.urls.custom_500_view'

from django.http import JsonResponse


def custom_404_view(request, exception):
    return JsonResponse({"message": 'Internet server error'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def custom_500_view(request):
    return JsonResponse({"message": 'Not found'},
                        status=status.HTTP_404_NOT_FOUND)
