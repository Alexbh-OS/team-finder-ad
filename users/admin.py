from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("email", "name", "surname", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active")
    search_fields = ("email", "name", "surname")
    ordering = ("email",)

    fieldsets = BaseUserAdmin.fieldsets + (
        ("Дополнительная информация", {
            "fields": (
                "name",
                "surname",
                "phone",
                "avatar",
                "github_url",
                "about",
                "skills",
            )
        }),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {
            "fields": ("name", "surname", "email", "phone"),
        }),
    )




