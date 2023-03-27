from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from .tasks import send_response
from .models import Statement
from .serializers import (
    MentiStatementSerializer,
    UpdateStatementSerializer,
    StatementSerializer
    )


class MentiStatementView(APIView):
    @swagger_auto_schema(request_body=MentiStatementSerializer)
    def post(self, request):
        serializer = MentiStatementSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.create(validated_data=serializer.validated_data)
            return Response(
                'Вы успешно отправили заявку ментору',
                status=status.HTTP_201_CREATED)
        

class UpdateDeleteStatementView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=UpdateStatementSerializer)
    def patch(self, request, id):
        statement = Statement.objects.filter(id=id).first()
        if not statement:
            return Response(
                'Заявления под таким id не существует!', 
                status=status.HTTP_404_NOT_FOUND
                )
        if request.user == statement.mentor_service:
            serializer = UpdateStatementSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.update(
                    instance=statement, 
                    validated_data=serializer.validated_data
                    )
                return Response(
                    data=serializer.data, 
                    status=status.HTTP_200_OK
                    )
        return Response(
            'Отказано в доступе!',
            status=status.HTTP_423_LOCKED
            )


    def delete(self, request, id):
        statement = Statement.objects.filter(id=id).first()
        if not statement:
            return Response(
                'Заявления под таким id не существует!', 
                status=status.HTTP_404_NOT_FOUND
                )
        if request.user == statement.mentor_service:
            statement.delete()
            return Response(
                'Заявка удалена!', 
                status=status.HTTP_204_NO_CONTENT
                )
        return Response(
            'Отказано в доступе!',
            status=status.HTTP_423_LOCKED
            )


class StatementAcceptedView(APIView):
    def get(self, request, accepted_code):
        statement = Statement.objects.filter(accepted_code=accepted_code).first()
        if not statement:
            return Response(
                'Что бы изменить свой ответ перейдите на наш сайт!', 
                status=status.HTTP_404_NOT_FOUND
                )
        statement.accepted = True
        statement.denied = False
        statement.accepted_code = ''
        statement.denied_code = ''
        statement.save()
        send_response(
            email=statement.mentor_service.email, 
            mentor=statement.mentor_service.username, 
            response=True
            )
        return Response(
            'Вы одобрили заявку менти!',
            status=status.HTTP_200_OK)


class StatementDeniedView(APIView):
    def get(self, request, denied_code):
        statement =  Statement.objects.filter(denied_code=denied_code).first()
        if not statement:
            return Response(
                'Что бы изменить свой ответ перейдите на наш сайт!', 
                status=status.HTTP_404_NOT_FOUND
                )
        statement.denied = True
        statement.accepted = False
        statement.accepted_code = ''
        statement.denied_code = ''
        statement.save()
        send_response(
            email=statement.mentor_service.email, 
            mentor=statement.mentor_service.username, 
            response=False
            )
        return Response(
            'Вы отклонили заявку менти!',
            status=status.HTTP_200_OK
            )


class GetStatementViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = Statement.objects.filter(mentor_service=request.user)
        serializer = StatementSerializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)