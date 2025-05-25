from django.contrib import admin

from .models import Category, Location, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Настройки для отображения, поиска, фильтраций в админке"""

    list_display = (
        'title',
        'pub_date',
        'author',
        'location',
        'category',
        'is_published',
        'image'
    )
    list_editable = (
        'category',
        'is_published'
    )
    search_fields = ('title',)
    list_filter = ('category',)
    list_display_links = ('title',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'description',
        'slug',
    )
    list_editable = (
        'description',
        'slug',
    )
    search_fields = ('title',)
    list_filter = ('slug',)
    list_display_links = ('title',)


admin.site.register(Location)
