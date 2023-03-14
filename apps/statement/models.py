from django.db import models
from datetime import datetime


class Statement(models.Model):
    JUNIOR = 'JN'
    MIDDLE = 'MD'
    SENIOR = 'SR'
    LEVEL = [
        (JUNIOR, 'Junior'),
        (MIDDLE, 'Middle'),
        (SENIOR, 'Senior'),
    ]
    my_level = models.CharField(
        max_length=2,
        choices=LEVEL,
        default=JUNIOR,
        )
    service = models.ForeignKey(
        to='service.Service', 
        on_delete=models.CASCADE, 
        related_name='statement_service'
    )
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=13, null=True, blank=True)
    description = models.TextField()
    create_at = models.DateTimeField(blank=True, default=datetime.now())

    def __str__(self) -> str:
        return f"{self.name} {self.email}"
    

class ResponseStatement(models.Model):
    statement = models.ForeignKey(
        to=Statement, 
        on_delete=models.CASCADE, 
        related_name='res_statement'
        )
    accepted = models.BooleanField()
    denied = models.BooleanField()
    message = models.CharField(max_length=500, blank=True, null=True)


    def __str__(self) -> str:
        return f"{self.statement.name} {self.accepted}"