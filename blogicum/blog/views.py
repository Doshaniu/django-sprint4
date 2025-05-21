from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .constants import POST_LIMIT_ON_PAGE
from .models import Category, Post


def index(request):
    """Главная страница с лентой постов, отсортированная по дате публикации."""
    template_name = 'blog/index.html'
    posts = Post.objects.filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now()
    )[:POST_LIMIT_ON_PAGE]
    context = {'posts': posts}
    return render(request, template_name, context)


def post_detail(request, pk):
    """Детальное описание поста по его идентификатору."""
    post = get_object_or_404(
        Post,
        pk=pk,
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True
    )
    template_name = 'blog/detail.html'
    context = {'post': post}
    return render(request, template_name, context)


def category_posts(request, category_slug):
    """Страница с постами отсортированными по категории."""
    template_name = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    post_list = category.posts.filter(
        is_published=True,
        pub_date__lte=timezone.now()
    ).order_by('-pub_date')
    context = {
        'category': category,
        'post_list': post_list
    }

    return render(request, template_name, context)
