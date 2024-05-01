from django.contrib import admin
from .models import *

# Register your models here.
from .models import UserProfile


class UserAdmin(admin.ModelAdmin):
   list_display = ("user", "role", "site_admin")

admin.site.register(UserProfile, UserAdmin)
admin.site.register(Report)
