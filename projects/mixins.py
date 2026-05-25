from django import forms
from projects.settings import GITHUB_URL_PREFIX
import re


class GitHubValidationMixin:
    """Mixin для валидации GitHub URL."""

    def clean_github_url(self):
        url = self.cleaned_data.get('github_url')

        if not url:
            return url

        url = url.rstrip('/')
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        github_pattern = r'^https?://(www\.)?github\.com/[\w.-]+/?$'
        if not re.match(github_pattern, url):
            raise forms.ValidationError(
                'Введите корректную ссылку на GitHub профиль '
                '(например, https://github.com/username)'
            )
