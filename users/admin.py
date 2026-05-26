from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html

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

    def avatar_preview(self, obj):
        """Возвращает HTML-код для отображения миниатюры аватара"""
        if obj.avatar:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 50%; object-fit: cover;" />',
                obj.avatar.url
            )
        return "Нет аватара"
    avatar_preview.short_description = "Аватар"
