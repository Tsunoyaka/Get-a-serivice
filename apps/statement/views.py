from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

from .models import Statement, ResponseStatement
from .serializers import StatementSerializer, ResponseStatementSerializer

class StatementViewSet(ModelViewSet):
    queryset = Statement.objects.all()
    serializer_class = StatementSerializer


class CreateResponseStatementView(APIView):
    @swagger_auto_schema(request_body=ResponseStatementSerializer)
    def post(self, request: Response):
        serializer = ResponseStatementSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.email(validated_data=serializer.validated_data)
            return Response(data=serializer.data, 
                            status=status.HTTP_201_CREATED
                            )

   
class DeleteResponseStatementView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request: Response, pk):
        queryset = ResponseStatement.objects.filter(statement__user=request.user, id=pk)
        if queryset.exists():
            queryset.delete()
            return Response(data='Заявление успешно удалено', 
                            status=status.HTTP_204_NO_CONTENT
                            )
        else:
            return Response(
                data='Такого заявления не сущестует!', 
                status=status.HTTP_404_NOT_FOUND
                )
