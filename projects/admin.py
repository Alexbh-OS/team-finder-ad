from django.contrib import admin

from projects.models import Project, Skill


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("name", "description", "owner__email", "owner__name")
    filter_horizontal = ("participants",)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

    def projects_count(self, obj):
        """Возвращает количество проектов, связанных с навыком"""
        return obj.projects.count()
    projects_count.short_description = "Количество проектов"
