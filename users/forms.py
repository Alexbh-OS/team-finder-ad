from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from projects.mixins import GitHubValidationMixin
from users.models import User


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("name", "surname", "email", "phone")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "input-field"


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "input-field"})
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"class": "input-field"})
    )


class UserProfileEditForm(GitHubValidationMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "name",
            "surname",
            "phone",
            "github_url",
            "about",
            "avatar",
            "skills",
        ]
        labels = {
            "name": "Имя",
            "surname": "Фамилия",
            "phone": "Телефон",
            "github_url": "Ссылка на GitHub",
            "about": "О себе",
            "avatar": "Фото профиля",
            "skills": "Ваши профессиональные навыки",
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "input-field"}),
            "surname": forms.TextInput(attrs={"class": "input-field"}),
            "phone": forms.TextInput(attrs={"class": "input-field"}),
            "github_url": forms.URLInput(attrs={"class": "input-field"}),
            "about": forms.Textarea(attrs={"class": "input-field", "rows": 4}),
            "avatar": forms.FileInput(attrs={"class": "input-field"}),
            "skills": forms.CheckboxSelectMultiple(),
        }

        

