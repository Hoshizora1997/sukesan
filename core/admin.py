from django.contrib import admin
from core.models import UserData, PlanDetail, Plan, Mob

@admin.register(UserData)
class UserData(admin.ModelAdmin):
    pass

@admin.register(PlanDetail)
class PlanDetail(admin.ModelAdmin):
    pass

@admin.register(Plan)
class Plan(admin.ModelAdmin):
    pass

@admin.register(Mob)
class Mob(admin.ModelAdmin):
    pass