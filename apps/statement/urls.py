from django.urls import path
from .views import StatementViewSet, CreateResponseStatementView, DeleteResponseStatementView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('crud', StatementViewSet)

urlpatterns = [
    path('create-response/', CreateResponseStatementView.as_view()),
    path('delete-response/<int:pk>', DeleteResponseStatementView.as_view())
]

urlpatterns += router.urls