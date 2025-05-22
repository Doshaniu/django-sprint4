from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.views.generic import DetailView, ListView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.core.paginator import Paginator

from .constants import POST_LIMIT_ON_PAGE
from .models import Category, Post


# def index(request):
#     """Главная страница с лентой постов, отсортированная по дате публикации."""
#     template_name = 'blog/index.html'
#     posts = Post.objects.filter(
#         is_published=True,
#         category__is_published=True,
#         pub_date__lte=timezone.now()
#     )[:POST_LIMIT_ON_PAGE]
#     context = {'posts': posts}
#     return render(request, template_name, context)


class HomePageListView(ListView):
    """Главная страница с лентой постов, отсортированная по дате публикации."""

    model = Post
    paginate_by = POST_LIMIT_ON_PAGE
    template_name = 'blog/index.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now()
        )


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


# def category_posts(request, category_slug):
#     """Страница с постами отсортированными по категории."""
#     template_name = 'blog/category.html'
#     category = get_object_or_404(
#         Category,
#         slug=category_slug,
#         is_published=True
#     )
#     post_list = category.posts.filter(
#         is_published=True,
#         pub_date__lte=timezone.now()
#     ).order_by('-pub_date')
#     context = {
#         'category': category,
#         'post_list': post_list
#     }

#     return render(request, template_name, context)


class CategoryPostsListView(ListView):
    """Страница с постами отсортированными по категории."""

    model = Post
    template_name = 'blog/category.html'
    paginate_by = POST_LIMIT_ON_PAGE

    def get_queryset(self):
        self.category = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True
        )
        return self.category.posts.filter(
            is_published=True,
            pub_date__lte=timezone.now()
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context

    
class RegisterCreationView(CreateView):
    template_name = 'registration/registration_form.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('blog:index')


class ProfileDetailView(DetailView):
    template_name = 'blog/profile.html'
    model = User
    context_object_name = 'profile'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        posts = Post.objects.filter(
            author=user,
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now()
        )
        paginator = Paginator(posts, POST_LIMIT_ON_PAGE)
        page_number = self.request.GET.get('page')
        context['page_obj'] = paginator.get_page(page_number)
        context['posts'] = posts
        return context


class CustomLogoutView(LogoutView):
    http_method_names = ['get', 'post', 'options']

    def get(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
