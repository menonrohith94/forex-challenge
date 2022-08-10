from rest_framework import serializers
from challenge.models import ForexConvert

class ForexSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForexConvert
        fields = '__all__'
