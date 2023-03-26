from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer
from apps.statement.serializers import StatementSerializer
from .models import Specialization

User = get_user_model()



class PersonalProfileSerializer(ModelSerializer):

    class Meta:
        model = User
        exclude = ('last_login','password','id','is_active','is_staff','activation_code')


class PublicProfileSerializer(ModelSerializer):

    class Meta:
        model = User
        exclude = ('last_login','password','id','is_active','is_staff','activation_code','email','telegram','telegram_status','registration_date')


class SpecializationSerializer(ModelSerializer):
    class Meta:
        model = Specialization
        fields = '__all__'


class MentorSerializer(ModelSerializer):

    class Meta:
        model = User
        exclude = ('last_login','password','id','is_active','is_staff','activation_code','email','telegram','telegram_status','registration_date')