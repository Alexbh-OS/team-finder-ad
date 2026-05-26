import random
from io import BytesIO

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.files.base import ContentFile
from django.db import models
from PIL import Image, ImageDraw, ImageFont

from users.settings import (
    MAX_ABOUT_LENGTH,
    MAX_PHONE_LENGTH,
    MAX_USNAME_LENGTH,
    AVATAR_IMAGE_SIZE,
    DEFAULT_AVATAR_COLOR,
    AVATAR_TEXT_COLOR,
    AVATAR_TEXT_POSITION,
    AVATAR_FONT_SIZE,
)
from users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name="Email адрес",
        unique=True
    )

    name = models.CharField(
        verbose_name="Имя",
        max_length=MAX_USNAME_LENGTH
    )

    surname = models.CharField(
        verbose_name="Фамилия",
        max_length=MAX_USNAME_LENGTH
    )
    avatar = models.ImageField(
        verbose_name="Фото профиля",
        upload_to="avatars/",
        blank=True
    )
    phone = models.CharField(
        verbose_name="Телефон",
        max_length=MAX_PHONE_LENGTH
    )
    github_url = models.URLField(
        verbose_name="Ссылка на GitHub",
        blank=True,
        null=True
    )
    about = models.TextField(
        verbose_name="О себе",
        max_length=MAX_ABOUT_LENGTH,
        blank=True,
        null=True
    )
    is_active = models.BooleanField(
        verbose_name="Активен",
        default=True
    )
    is_staff = models.BooleanField(
        verbose_name="Статус персонала",
        default=False
    )
    skills = models.ManyToManyField(
        "projects.Skill",
        related_name="users",
        blank=True,
        verbose_name="Профессиональные навыки"
    )
    favorites = models.ManyToManyField(
        "projects.Project",
        related_name="favorited_by",
        blank=True,
        verbose_name="Избранные проекты"
    )

    objects = UserManager()

    USER_FIELD = "email"
    REQUIRED_FIELDS = ["name", "surname", "phone"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.name} {self.surname} ({self.email})"

    def save(self, *args, **kwargs):
        if not self.avatar:
            self.create_avatar()
        super().save(*args, **kwargs)

    def create_avatar(self):
        """Генерирует аватар с инициалами пользователя"""
        low, high = DEFAULT_AVATAR_COLOR
        color = (
            random.randint(low, high),
            random.randint(low, high),
            random.randint(low, high)
        )
        img = Image.new('RGB', AVATAR_IMAGE_SIZE, color=color)
        draw = ImageDraw.Draw(img)

        draw.rectangle((0, 0, 199, 199), outline=(0, 0, 0), width=2)

        letter = self.name[0].upper() if self.name else 'U'

        try:
            font = ImageFont.truetype('arial.ttf', AVATAR_FONT_SIZE)
        except (IOError, OSError):
            try:
                font = ImageFont.load_default()
                font = font.font_variant(size=AVATAR_FONT_SIZE)
            except AttributeError:
                font = ImageFont.load_default()

        draw.text(
            AVATAR_TEXT_POSITION,
            letter,
            fill=AVATAR_TEXT_COLOR,
            font=font
        )

        buffer = BytesIO()
        img.save(buffer, format='PNG')
        filename = f'{self.email.split("@")[0]}_avatar.png'
        self.avatar.save(filename, ContentFile(buffer.getvalue()), save=False)
