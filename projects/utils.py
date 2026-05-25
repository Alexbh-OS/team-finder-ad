from django.core.paginator import Paginator
from projects.settings import PAGINATION_PAGE_SIZE


def get_paginated_page(request, queryset, page_size=PAGINATION_PAGE_SIZE):
    paginator = Paginator(queryset, page_size)
    page_number = request.GET.get("page")
    return paginator.get_page(page_number)