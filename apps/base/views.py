from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView

from .serializers import MentorSerializer, SpecializationSerializer
from .models import Specialization

from .serializers import (
    PersonalProfileSerializer, 
    PublicProfileSerializer,
    )

User = get_user_model()


class PersonalProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = get_object_or_404(User, id=self.request.user.id)
        serializer = PersonalProfileSerializer(profile)
        return Response(serializer.data)


class PublicProfileView(APIView):
    def get(self, request,pk):
        profile = get_object_or_404(User, id=pk)
        serializer = PublicProfileSerializer(profile)
        return Response(serializer.data)


class SpecializationViewSet(ModelViewSet):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer
    permission_classes = [IsAdminUser]


class ListOfMentorsView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = MentorSerializer

