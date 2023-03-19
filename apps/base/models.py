from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Stack(models.Model):
    title = models.CharField(max_length=100, unique=True,verbose_name='Стек')

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name = "Стек"
        verbose_name_plural = "Стеки"


# class UserStack(models.Model):
#     stack = models.CharField(max_length=100, verbose_name='Стек')
#     user = models.ForeignKey(Stack, on_delete=models.CASCADE, related_name='user_stack')

#     def __str__(self) -> str:
#         return self.stack
    
#     class Meta:
#         verbose_name = "Юзер Стек"
#         verbose_name_plural = "Юзер Стеки"



