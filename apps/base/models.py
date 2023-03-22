from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Specialization(models.Model):
    title = models.CharField(max_length=64)

    def __str__(self) -> str:
        return self.title