from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.HomePageListView.as_view(), name='index'),
    path(
        'posts/<int:pk>/',
        views.PostDetailView.as_view(),
        name='post_detail'
    ),
    path(
        'category/<slug:category_slug>/',
        views.CategoryPostsListView.as_view(),
        name='category_posts'
    ),
    path(
        'auth/registration/',
        views.RegisterCreationView.as_view(),
        name='registration'
    ),
    path(
        'profile/<str:username>/',
        views.ProfileDetailView.as_view(),
        name='profile'),
    path('posts/create/', views.CreatePostView.as_view(), name='create'),
    path(
        'posts/<int:pk>/edit/', views.PostEditView.as_view(), name='post_edit'
    ),
    path(
        'posts/<int:post_id>/comment/',
        views.CommentCreateView.as_view(),
        name='add_comment'
    ),
    path(
        'posts/<int:post_id>/edit_comment/<int:comment_id>/',
        views.CommentEditView.as_view(),
        name='comment_edit'
    )
]
