from django.urls import path
from .views import ( 
    MentiStatementView,
    StatementAcceptedView,
    StatementDeniedView,
    UpdateDeleteStatementView,
    GetStatementViewSet
    )


urlpatterns = [
    path('menti-statement/', MentiStatementView.as_view()),
    path('accepted-email/<str:accepted_code>/', StatementAcceptedView.as_view()),
    path('denied-email/<str:denied_code>/', StatementDeniedView.as_view()),
    path('update-delete/<int:id>/', UpdateDeleteStatementView.as_view()),
    path('my-statement/', GetStatementViewSet.as_view()),
]
