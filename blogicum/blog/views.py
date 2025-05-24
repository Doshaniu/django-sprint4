from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import DeleteView, DetailView, ListView, UpdateView
from django.views.generic.edit import CreateView

from .constants import POST_LIMIT_ON_PAGE
from .custom_mixins import CustomAuthorMixin
from .forms import CommentForm, ProfileEditForm
from .models import Category, Comment, Post


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
        ).annotate(comment_count=Count('comments')).order_by('-pub_date')


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
    """Страница профиля пользователя с его постами."""

    template_name = 'blog/profile.html'
    model = User
    context_object_name = 'profile'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        if self.request.user == user:
            posts = Post.objects.filter(author=user)
        else:
            posts = Post.objects.filter(
                author=user,
                is_published=True,
                category__is_published=True,
                pub_date__lte=timezone.now()
            )
        posts = posts.annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date')
        paginator = Paginator(posts, POST_LIMIT_ON_PAGE)
        page_number = self.request.GET.get('page')
        context['page_obj'] = paginator.get_page(page_number)
        context['can_edit'] = self.request.user == user
        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    """Страница редактирования профиля пользователя."""

    model = User
    form_class = ProfileEditForm
    template_name = 'blog/user.html'
    success_url = reverse_lazy('blog:profile')

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile', kwargs={'username': self.request.user.username})


class CustomLogoutView(LogoutView):
    http_method_names = ['get', 'post', 'options']

    def get(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CreatePostView(LoginRequiredMixin, CreateView):
    """Страница для создания поста."""

    model = Post
    template_name = 'blog/create.html'
    fields = [
        'title', 'text', 'location', 'category', 'image', 'pub_date']

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user.username})

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDetailView(DetailView):
    """Страница детального описания поста,
    с комментариями.
    """

    model = Post
    template_name = 'blog/detail.html'

    def get_object(self):
        user = self.request.user
        if user.is_authenticated:
            condition = (
                Q(author=self.request.user)
                | (Q(is_published=True)
                    & Q(category__is_published=True)
                    & Q(pub_date__lte=timezone.now()))
            )
        else:
            condition = (
                Q(is_published=True)
                & Q(category__is_published=True)
                & Q(pub_date__lte=timezone.now())
            )
        post = get_object_or_404(
            Post.objects.filter(condition),
            pk=self.kwargs['post_id'],
        )
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['form'] = CommentForm()
        context['comments'] = (
            self.object.comments.select_related('author').all()
        )
        return context


class PostEditView(CustomAuthorMixin, UpdateView):
    """Страница редактирования поста."""

    model = Post
    fields = ['title', 'text', 'category', 'location', 'image', 'pub_date']
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail', kwargs={'post_id': self.object.pk}
        )


class PostDeleteView(CustomAuthorMixin, DeleteView):
    """Страница удаления поста."""

    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user.username})


class CommentCreateView(LoginRequiredMixin, CreateView):
    """Создание комментария к посту,
    с проверкой авторизации.
    """

    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['post_id']})


class CommentEditView(CustomAuthorMixin, UpdateView):
    """Редактирование комментария,
    с проверкой на авторство.
    """

    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['post_id']}
        )

    def get_object(self, queryset=None):
        return get_object_or_404(
            Comment,
            pk=self.kwargs['comment_id'],
            post_id=self.kwargs['post_id']
        )


class CommentDeleteView(CustomAuthorMixin, DeleteView):
    """Удаление комментария, с проверкой на авторство."""

    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail', kwargs={'post_id': self.object.post.pk}
        )
