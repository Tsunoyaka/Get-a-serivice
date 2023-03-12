from rest_framework.serializers import ModelSerializer

from .models import Service

class ServiceSerializer(ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

    def to_representation(self, instance):
        return super().to_representation(instance)
    
    def validate(self, attrs):
        attrs = super().validate(attrs)
        return attrs
    


        