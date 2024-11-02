from django.contrib import admin
from core.models import SmdUser
# Register your models here.


@admin.register(SmdUser)
class AdminSmdUser(admin.ModelAdmin):
    list_display = ('email','level')
