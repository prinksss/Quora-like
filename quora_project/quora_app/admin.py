from django.contrib import admin
from .models import Question,Answer,Like
from django.contrib.auth.models import User

from django.contrib.auth import get_user_model

# Register your models here.
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Like)

User = get_user_model()

class CustomUserAdmin(admin.ModelAdmin):
    pass
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)