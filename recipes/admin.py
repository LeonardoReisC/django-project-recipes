from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline

from .models import Category, Recipe
from tag.models import Tag


# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    ...


class TagInline(GenericStackedInline):
    model = Tag
    fields = ['name']
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at', 'is_published', 'author']
    list_display_links = 'title', 'created_at'
    search_fields = 'id', 'title', 'description', 'slug', 'preparation_steps'
    list_filter = 'category', 'author', 'is_published', \
        'preparation_steps_is_html'
    list_per_page = 10
    list_editable = 'is_published',
    ordering = '-id',
    prepopulated_fields = {
        'slug': ('title',)
    }
    inlines = [
        TagInline
    ]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Recipe, RecipeAdmin)
