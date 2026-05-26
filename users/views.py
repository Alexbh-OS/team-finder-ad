from django.urls import reverse
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from users.forms import UserProfileEditForm, UserRegistrationForm, UserLoginForm
from users.models import User

from users.settings import (
    PAGINATION_SIZE
)

class UserRegisterView(CreateView):
    """Регистрация нового пользователя"""
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('projects:list')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class UserLoginView(LoginView):
    """Аутентификация пользователя"""
    form_class = UserLoginForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('projects:list')


class UserLogoutView(LogoutView):
    """Выход из системы"""
    next_page = reverse_lazy('projects:list')


class ParticipantsListView(ListView):
    """Список всех участников"""
    model = User
    template_name = 'users/participants.html'
    context_object_name = 'participants'
    paginate_by = PAGINATION_SIZE

    def get_queryset(self):
        queryset = (
            User.objects
            .exclude(is_superuser=True)
            .prefetch_related('skills')
            .order_by('-id')
        )

        query = self.request.GET.get('q', '')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(surname__icontains=query)
            )

        active_filter = self.request.GET.get('filter', '')
        if self.request.user.is_authenticated and active_filter:
            queryset = self._apply_filter(queryset, active_filter)

        return queryset.distinct()

    def _apply_filter(self, queryset, active_filter):
        """Фильтры в зависимости от параметра"""
        user = self.request.user

        filters_map = {
            'owners-of-favorite-projects': lambda: queryset.filter(
                owned_projects__in=user.favorites.all()
            ),
            'owners-of-participating-projects': lambda: queryset.filter(
                owned_projects__participants=user
            ),
            'interested-in-my-projects': lambda: queryset.filter(
                favorites__owner=user
            ),
            'participants-of-my-projects': lambda: queryset.filter(
                participated_projects__owner=user
            ),
        }
        return filters_map.get(active_filter, lambda: queryset)()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['active_filter'] = self.request.GET.get('filter', '')
        return context


class UserDetailView(DetailView):
    """Просмотр профиля пользователя"""
    model = User
    template_name = 'users/user-details.html'
    context_object_name = 'profile'

    def get_queryset(self):
        return User.objects.prefetch_related('owned_projects', 'skills')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_projects'] = (
            self.object.owned_projects.all().order_by('-created_at')
        )
        context['skills'] = self.object.skills.all()
        return context


class UserProfileEditView(LoginRequiredMixin, UpdateView):
    """Редактирование профиля пользователя"""
    form_class = UserProfileEditForm
    template_name = 'users/edit_profile.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse(
            'users:profile_with_pk',
            kwargs={'pk': self.request.user.pk}
        )

