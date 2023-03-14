from rest_framework import serializers
from .models import Statement, ResponseStatement
from .tasks import send_response
from .validations import normalize_phone


class StatementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statement
        fields = ['name', 'my_level', 'email', 'phone', 'description', 'create_at']


    def validate_phone(self, phone):
        phone = normalize_phone(phone=phone)
        if len(phone) != 13:
            raise serializers.ValidationError('Неверный формат телефона')
        return phone


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        accepted = instance.res_statement.all()
        if accepted.count() > 0:
            representation['accepted'] = accepted[0].accepted
        return representation
    

class ResponseStatementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponseStatement
        fields = ['statement', 'accepted', 'denied', 'message']


    def validate(self, attrs):
        response = ResponseStatement.objects.filter(statement=attrs.get('statement')).exists()
        if response is True:
            raise serializers.ValidationError('Response already exist')
        accepted = attrs.get('accepted')
        denied = attrs.get('denied')
        if accepted is denied:
            raise serializers.ValidationError('Select field')
        return attrs
    
    
    def email(self, validated_data):
        try:
            email = validated_data['statement'].email
            send_response.delay(email=email, message=validated_data['message'], response=validated_data['accepted'])
        except KeyError:
            send_response.delay(email=email, message=' ', response=validated_data['accepted'])
        ResponseStatement.objects.create(**validated_data)
        


    
    