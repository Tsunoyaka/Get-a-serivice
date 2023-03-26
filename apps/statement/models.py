from django.db import models
from django.utils.crypto import get_random_string


class Statement(models.Model):
    my_level = models.CharField(max_length=10)
    mentor_service = models.ForeignKey(
        to='account.User',
        on_delete=models.CASCADE,
        related_name='mentor'
        )
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    telegram = models.CharField(max_length=255)
    description = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
    denied = models.BooleanField(default=False)
    accepted_code = models.CharField(max_length=10, blank=True)
    denied_code = models.CharField(max_length=10, blank=True)

    def create_response_code(self):
        code1 = get_random_string(length=10)
        code2 = get_random_string(length=10)
        if Statement.objects.filter(denied_code=code1).exists() or Statement.objects.filter(denied_code=code2).exists():
            self.create_response_code()
        self.denied_code = code1
        if Statement.objects.filter(accepted_code=code1).exists() or Statement.objects.filter(accepted_code=code2).exists():
            self.create_response_code()
        self.accepted_code = code2
        self.save()

    def __str__(self) -> str:
        return f"{self.name} {self.email}"