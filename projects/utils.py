from django.core.paginator import Paginator

from projects.settings import PAGINATION_PAGE_SIZE

from .models import Project


def get_optimized_project_queryset():
    """Возвращает оптимизированный QuerySet для Project"""
    return Project.objects.select_related('owner').prefetch_related(
        'skills', 'participants'
    )

def get_paginated_page(request, queryset, page_size=PAGINATION_PAGE_SIZE):
    """Возвращает страницу с пагинацией"""
    paginator = Paginator(queryset, page_size)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)
