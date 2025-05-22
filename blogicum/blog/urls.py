from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.HomePageListView.as_view(), name='index'),
    path('posts/<int:pk>/', views.post_detail, name='post_detail'),
    path('category/<slug:category_slug>/',
         views.CategoryPostsListView.as_view(), name='category_posts'),
    path(
        'auth/registration/',
        views.RegisterCreationView.as_view(),
        name='registration'
    ),
    path(
        'profile/<str:username>/',
        views.ProfileDetailView.as_view(),
        name='profile'),

]
