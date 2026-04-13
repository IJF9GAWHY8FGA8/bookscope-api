from rest_framework import serializers
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny

from bookscope.api import HealthCheckResponse


class HealthCheckSerializer(serializers.Serializer):
    status = serializers.CharField()
    service = serializers.CharField()


class HealthCheckAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = HealthCheckSerializer

    def get(self, request, *args, **kwargs):
        return HealthCheckResponse()
