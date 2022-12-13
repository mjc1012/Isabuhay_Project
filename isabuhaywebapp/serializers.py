from rest_framework import serializers
from isabuhaywebapp.models import CBCTestResultImage


class ScreenshotCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CBCTestResultImage
        fields = [
            'testImage'
        ]