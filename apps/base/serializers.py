from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer
from apps.statement.serializers import StatementSerializer
from apps.service.models import Service
from . models import Stack


User = get_user_model()



class PersonalProfileSerializer(ModelSerializer):

    class Meta:
        model = User
        exclude = ('last_login','password','id','is_active','is_staff','activation_code')


    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['services'] = ProfileServiceSerializer(
            instance.user_service.all(), many=True
        ).data
        
        return rep


class PublicProfileSerializer(ModelSerializer):

    class Meta:
        model = User
        exclude = ('last_login','password','id','is_active','is_staff','activation_code','email')


    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['services'] = ServiceSerializer(
            instance.user_service.all(), many=True
        ).data
        return rep


class ProfileServiceSerializer(ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['requests'] = StatementSerializer(
            instance.statement_service.all(), many=True
        ).data
        return rep


class StackSerializer(ModelSerializer):
    class Meta:
        model = Stack
        exclude = ('id',)
    

# class UserStackSerializer(ModelSerializer):
#     class Meta:
#         model = UserStack
#         fields = '__all__'


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