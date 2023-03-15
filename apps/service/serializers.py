from rest_framework.serializers import ModelSerializer
from .models import Service
from apps.base.serializers import StackSerializer


class ServiceSerializer(ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['stack'] = StackSerializer(
            instance.stack.all(), many=True
        ).data
        return rep

    
    def validate(self, attrs):
        attrs = super().validate(attrs)
        return attrs
    



        