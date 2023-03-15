from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import PersonalProfileView, PublicProfileView

router = DefaultRouter()



urlpatterns = [
    path('public-profile/<int:pk>/', PublicProfileView.as_view(), name='retrieve'),
    path('personal-profile/', PersonalProfileView.as_view(), name='profile')
]
urlpatterns += router.urls

