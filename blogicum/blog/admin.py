from django.contrib import admin

from .models import Category, Location, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Более гибкая и удобная админка для управления сайтом."""

    list_display = (
        'title',
        'pub_date',
        'author',
        'location',
        'category',
        'is_published'
    )
    list_editable = (
        'category',
        'is_published'
    )
    search_fields = ('title',)
    list_filter = ('category',)
    list_display_links = ('title',)


admin.site.register(Category)
admin.site.register(Location)
