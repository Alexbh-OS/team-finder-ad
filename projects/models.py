from django.conf import settings
from django.db import models
from django.urls import reverse

from projects.settings import (
    MAX_NAME_LEN,
    MAX_PJ_NAME_LEN,
    MAX_STAT_LEN,
    STATUS_CHOICES,
    ProjectStatus,
)


class Skill(models.Model):
    name = models.CharField(
        verbose_name="Название навыка",
        max_length=MAX_NAME_LEN,
        unique=True,
    )

    class Meta:
        verbose_name = "Навык"
        verbose_name_plural = "Навыки"

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(
        verbose_name="Название проекта",
        max_length=MAX_PJ_NAME_LEN,
    )
    description = models.TextField(
        verbose_name="Описание",
        blank=True,
        null=True,
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_projects",
        verbose_name="Владелец",
    )
    created_at = models.DateTimeField(
        verbose_name="Дата создания",
        auto_now_add=True,
    )
    github_url = models.URLField(
        verbose_name="Ссылка на GitHub",
        blank=True,
        null=True,
    )
    status = models.CharField(
        verbose_name="Статус",
        max_length=MAX_STAT_LEN,
        choices=STATUS_CHOICES,
        default=ProjectStatus.OPEN,
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="participated_projects",
        blank=True,
        verbose_name="Участники",
    )
    skills = models.ManyToManyField(
        Skill,
        related_name="projects",
        blank=True,
        verbose_name="Необходимые навыки",
    )

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("projects:detail", kwargs={"pk": self.pk})


