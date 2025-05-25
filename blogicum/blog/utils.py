from django.core.paginator import Paginator

from .constants import POST_LIMIT_ON_PAGE


def paginate_page(request, post_list, post_per_page=POST_LIMIT_ON_PAGE):
    """Функция для пагинации страниц"""
    paginator = Paginator(post_list, post_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
