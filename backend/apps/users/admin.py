from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CandidateProfile, CompanyProfile, User


@admin.register(User)
class CoreHireUserAdmin(UserAdmin):
    list_display = ("email", "username", "role", "is_staff")
    fieldsets = UserAdmin.fieldsets + (("Role", {"fields": ("role",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (("Role", {"fields": ("role",)}),)


admin.site.register(CandidateProfile)
admin.site.register(CompanyProfile)
