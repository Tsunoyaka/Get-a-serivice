from rest_framework import serializers
from .models import Statement
from .tasks import send_response, send_respons_mentor
from apps.django_bot.views import mentor_response


class StatementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statement
        exclude = ('accepted_code', 'denied_code')


class MentiStatementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statement
        fields = ('my_level', 'mentor_service', 'name', 'email', 'telegram', 'description')

    def create(self, validated_data):
        statement = Statement.objects.create(**validated_data)
        statement.create_response_code()
        send_respons_mentor(instance=statement)
        if statement.mentor_service.telegram_status is True:
            mentor_response(instance=statement)
        return statement
    

class UpdateStatementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statement
        fields = ('accepted', 'denied')

    def validate(self, attrs):
        accepted = attrs.get('accepted')
        denied = attrs.get('denied')
        if not attrs:
            raise serializers.ValidationError(
                'Please fill in the field'
            )
        elif accepted and denied is True:
            raise serializers.ValidationError(
                'Please select only one field'
                )
        elif accepted is False and denied is False:
            raise serializers.ValidationError(
                'Please select only one field'
                )
        if accepted is True:
            attrs['denied'] = False
        elif denied is True:
            attrs['accepted'] = False
        return attrs
    
    def update(self, instance: Statement, validated_data):
        send_response(instance=instance,
                      response=validated_data.get('accepted'))
        instance.accepted = validated_data.get('accepted', instance.accepted)
        instance.denied = validated_data.get('denied', instance.denied)
        instance.save()
        return instance