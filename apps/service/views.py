from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

from .models import Service
from .serializers import ServiceSerializer
 
User = get_user_model()

class ServiceViewSet(ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    
    
    def get_permissions(self):
        if self.action in ['retrive', 'list', 'search']:
            return []
        return [IsAuthenticated()]
    







    