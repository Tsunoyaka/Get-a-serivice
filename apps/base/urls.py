from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import PersonalProfileView, PublicProfileView, StackViewSet

router = DefaultRouter()
router.register('stack', StackViewSet)


urlpatterns = [
    path('public-profile/<int:pk>/', PublicProfileView.as_view(), name='retrieve'),
    path('personal-profile/', PersonalProfileView.as_view(), name='profile')
]
urlpatterns += router.urls

