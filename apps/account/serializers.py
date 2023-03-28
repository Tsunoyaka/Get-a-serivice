from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from apps.base.models import Specialization

from .tasks import send_activation_code


User = get_user_model()


def email_validator(email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'User with this email does not exist'
            )
        return email


class UserRegistrationSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(max_length=128, required=True)
    specialization = serializers.ListField()

    class Meta:
        model = User
        exclude = ('telegram', 'telegram_status', 'last_login','id','is_active','is_staff',
                   'activation_code', 'status', 'registration_date')


    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'Email already in use'
            )
        return email


    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('Passwords do not match')
        return attrs

    def create(self, validated_data):
        specializations = validated_data.pop('specialization')
        sp = []
        for specialization in specializations:
            sp.append(Specialization.objects.filter(title=specialization).first())
        user = User.objects.create_user(**validated_data)
        user.specialization.set(sp)
        user.create_activation_code()
        send_activation_code(user.email, user.activation_code)
        return user
    

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128, required=True)
    new_password = serializers.CharField(max_length=128, required=True)
    new_pass_confirm = serializers.CharField(max_length=128, required=True)

    def validate_old_password(self, old_password):
        user = self.context.get('request').user
        if not user.check_password(old_password):
            raise serializers.ValidationError(
                'Wrong password'
            )
        return old_password
    
    def validate(self, attrs: dict):
        new_password = attrs.get('new_password')
        new_pass_confirm = attrs.get('new_pass_confirm')
        if new_password != new_pass_confirm:
            raise serializers.ValidationError('Passwords do not match')
        return attrs

    def set_new_password(self):
        user = self.context.get('request').user
        password = self.validated_data.get('new_password')
        user.set_password(password)
        user.save()


class RestorePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True, 
        max_length=255, 
        validators=[email_validator]
        )

    def send_code(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.create_activation_code()
        send_mail(
            subject='Password restore',
            message=f'Your code for password restore {user.activation_code}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email]
        )

    def send_email_code(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.create_activation_code()
        send_mail(
            subject='Change email',
            message=f'Your code for ghange email {user.activation_code}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email]
        )


class SetRestoredPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True, 
        max_length=255,
        validators=[email_validator]
        )
    code = serializers.CharField(min_length=1, max_length=8, required=True)
    new_password = serializers.CharField(max_length=128, required=True)
    new_pass_confirm = serializers.CharField(max_length=128, required=True)

    def validate_code(self, code):
        if not User.objects.filter(activation_code=code).exists():
            raise serializers.ValidationError(
                'Wrong code'
            )
        return code

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        new_pass_confirm = attrs.get('new_pass_confirm')
        if new_password != new_pass_confirm:
            raise serializers.ValidationError(
                'Passwords do not match'
            )
        return attrs
        
    def set_new_password(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        new_password = self.validated_data.get('new_password')
        user.set_password(new_password)
        user.activation_code = ''
        user.save()


class UpdateUsernameImageSerializer(serializers.ModelSerializer):
    specialization = serializers.ListField()

    def validate(self, attrs):
        user = self.context['request'].user
        attrs['user'] = user
        return attrs


    class Meta:
        model = User
        exclude = ('id', 'email', 'last_login', 'is_active', 'is_staff', 
                   'activation_code', 'status', 'password', 'registration_date')
        
        extra_kwargs = {'username': {'required': False}, 'image': {'required': False}, 
                        'position': {'required': False}, 'place_of_work': {'required': False}, 
                        'about_me': {'required': False}, 'help': {'required': False}, 
                        'level_mentor': {'required': False}, 'experience': {'required': False},
                        'skills': {'required': False}, 'price': {'required': False}, 
                        'language': {'required': False}}


    def update(self, instance: User, validated_data):
        specializations = validated_data.get('specialization')
        sp = []
        for specialization in specializations:
            sp.append(Specialization.objects.filter(title=specialization).first())
        instance.username = validated_data.get('username', instance.username) 
        instance.image = validated_data.get('image', instance.image)
        instance.position = validated_data.get('position', instance.position)
        instance.place_of_work = validated_data.get('place_of_work', instance.place_of_work)
        instance.about_me = validated_data.get('place_of_work', instance.place_of_work)
        instance.help = validated_data.get('help', instance.help)
        instance.level_mentor = validated_data.get('level_mentor', instance.level_mentor)
        instance.experience = validated_data.get('experience', instance.experience)
        instance.skills = validated_data.get('skills', instance.skills)
        instance.price = validated_data.get('price', instance.price)
        instance.language = validated_data.get('language', instance.language)
        instance.telegram = validated_data.get('telegram', instance.telegram)
        instance.telegram_status = validated_data.get('telegram_status', instance.telegram_status)
        if specialization:
            instance.specialization.set(sp)
        instance.save()


class AccountDeleteSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, required=True)
    password = serializers.CharField(max_length=128, required=True)


    def validate(self, attrs):
        user = self.context.get('request').user
        if user.email != attrs.get('email'):
            raise serializers.ValidationError(
                'Wrong email'
            )        
        if not user.check_password(attrs.get('password')):
            raise serializers.ValidationError(
                'Wrong password'
            )
        return attrs


class UpdateEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=255)
    password =serializers.CharField(max_length=128, required=True)

    def validate(self, attrs):
        user = self.context.get('request').user
        if not user.check_password(attrs.get('password')):
            raise serializers.ValidationError(
                'Wrong password'
            )
        return attrs

    def update(self, instance: User, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance