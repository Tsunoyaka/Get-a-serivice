from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from django.contrib.auth import get_user_model
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .serializers import (
    UserRegistrationSerializer, 
    PasswordChangeSerializer,
    RestorePasswordSerializer,
    SetRestoredPasswordSerializer,
    UpdateUsernameImageSerializer,
    UpdateEmailSerializer,
    AccountDeleteSerializer
    )


User = get_user_model()


class RegistrationView(APIView):
    @swagger_auto_schema(request_body=UserRegistrationSerializer)
    def post(self, request: Request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                'Спасибо за регистрацию! Ссылка для активации учетной записи отправлена Вам на почту.',
                status=status.HTTP_201_CREATED
            )


class AccountActivationView(APIView):
    def get(self, request, activation_code):
        user = User.objects.filter(activation_code=activation_code).first()
        if not user:
            return Response(
                'Страница не найдена...', 
                status=status.HTTP_404_NOT_FOUND
                )
        user.is_active = True
        user.activation_code = ''
        user.save()
        return Response(
            'Учетная запись активирована! Теперь Вы можете войти на ...', 
            status=status.HTTP_200_OK
            )


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()
            return Response(
                'Ваш пароль успешно изменен.',
                status=status.HTTP_200_OK
            )


class RestorePasswordView(APIView):
    def post(self, request: Request):
        serializer = RestorePasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.send_code()
            return Response(
                'Код для восстановления пароля был отправлен Вам на почту.',
                status=status.HTTP_200_OK
            )


class NewEmailView(APIView):
    def post(self, request: Request):
        serializer = RestorePasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.send_email_code()
            return Response(
                'Код для изменения почты был отправлен вам на почту.',
                status=status.HTTP_200_OK
            )


class SetRestoredPasswordView(APIView):
    def post(self, request: Request):
        serializer = SetRestoredPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()
            return Response(
                'Ваш пароль успешно восстановлен.',
                status=status.HTTP_200_OK
            )


class SetNewEmailView(APIView):
    def post(self, request: Request):
        serializer = UpdateEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.update()
            return Response(
                'Ваша почта успешно изменена.',
                status=status.HTTP_200_OK
            )


class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]    

    def post(self, request: Request):
        email = request.user.email
        serializer = AccountDeleteSerializer(data = request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            User.objects.get(email=email).delete()
            return Response(
                'Ваш аккаунт успешно удален!',
                status=status.HTTP_204_NO_CONTENT
            )



class UserPatchUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(request_body=UpdateUsernameImageSerializer)
    def patch(self, request):
        email = request.user.email
        obj = User.objects.get(email=email)
        serializer = UpdateUsernameImageSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.update(obj, serializer.validated_data)
            answer = {"status": "UPDATE" }
            answer.update(serializer.data, status=status.HTTP_200_OK)
            return Response(answer)