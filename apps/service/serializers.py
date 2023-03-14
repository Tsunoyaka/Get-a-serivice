from rest_framework.serializers import ModelSerializer
from .models import Service, Stack, StackService, UserStack

class ServiceSerializer(ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

    def to_representation(self, instance):
        return super().to_representation(instance)
    
    def validate(self, attrs):
        attrs = super().validate(attrs)
        return attrs
    

class StackSerializer(ModelSerializer):
    class Meta:
        model = Stack
        fields = '__all__'

    def to_representation(self, instance):
        return super().to_representation(instance)
    
    def validate(self, attrs):
        attrs = super().validate(attrs)
        return attrs
    

class StackServiceSerializer(ModelSerializer):
    class Meta:
        model = StackService
        fields = '__all__'

    def to_representation(self, instance):
        return super().to_representation(instance)
    
    def validate(self, attrs):
        attrs = super().validate(attrs)
        return attrs


class UserStackSerializer(ModelSerializer):
    class Meta:
        model = UserStack
        fields = '__all__'

    def to_representation(self, instance):
        return super().to_representation(instance)
    
    def validate(self, attrs):
        attrs = super().validate(attrs)
        return attrs
    
        