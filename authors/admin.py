from django.contrib import admin

from .models import Profile

# Register your models here.


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = 'author_first_name',

    @admin.display(ordering='author__first_name')
    def author_first_name(self, obj):
        return obj.author.first_name
