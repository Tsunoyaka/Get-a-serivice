from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ServiceViewSet, StackViewSet, StackServiceViewSet, UserStackViewSet

router = DefaultRouter()
router.register('service', ServiceViewSet)
router.register('stack', StackViewSet)
router.register('stack_service', StackServiceViewSet)
router.register('user_stack', UserStackViewSet)


urlpatterns =[
    path('', include(router.urls)),
]
