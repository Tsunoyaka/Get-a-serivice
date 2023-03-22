from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer
from apps.statement.serializers import StatementSerializer
from .models import Stack


User = get_user_model()



class PersonalProfileSerializer(ModelSerializer):

    class Meta:
        model = User
        exclude = ('last_login','password','id','is_active','is_staff','activation_code')


class PublicProfileSerializer(ModelSerializer):

    class Meta:
        model = User
        exclude = ('last_login','password','id','is_active','is_staff','activation_code','email')


class StackSerializer(ModelSerializer):
    class Meta:
        model = Stack
        fields = '__all__'

