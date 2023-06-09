from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import PersonalProfileView, PublicProfileView, SpecializationViewSet, ListOfMentorsView


router = DefaultRouter()
router.register('specialization', SpecializationViewSet)


urlpatterns = [
    path('public-profile/<int:pk>/', PublicProfileView.as_view(), name='retrieve'),
    path('personal-profile/', PersonalProfileView.as_view(), name='profile'),
    path('mentors/', ListOfMentorsView.as_view())
]


urlpatterns += router.urls