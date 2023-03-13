from django.contrib import admin
from .models import Service, Stack, StackService, UserStack

admin.site.register(Service)
admin.site.register(Stack)
admin.site.register(StackService)
admin.site.register(UserStack)



