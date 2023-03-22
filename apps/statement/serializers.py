from rest_framework import serializers
from .models import Statement, ResponseStatement
from .tasks import send_response, send_statement


class StatementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statement
        fields = ['mentor_service', 'name', 'my_level', 'email', 
                  'telegram', 'description', 'create_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        accepted = instance.res_statement.all()
        if accepted.count() > 0:
            representation['accepted'] = accepted[0].accepted
        return representation
    
    def create(self, validated_data):
        mentor_email = validated_data.get('mentor_service').email
        name = validated_data.get('name')
        send_statement.delay(email=mentor_email, name=name)
        return super().create(validated_data)


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