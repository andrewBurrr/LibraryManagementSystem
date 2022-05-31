from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Genre, Format, Language, Author, Item, ItemInstance
from .models import CustomUser
# Register your models here.


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username', ]


class GenreAdmin(admin.ModelAdmin):
    exclude = ('slug',)


class FormatAdmin(admin.ModelAdmin):
    exclude = ('slug',)


class LanguageAdmin(admin.ModelAdmin):
    exclude = ('slug',)


class AuthorAdmin(admin.ModelAdmin):
    exclude = ('slug',)


class ItemAdmin(admin.ModelAdmin):
    exclude = ('slug',)
    list_display = ('title', 'format', 'created', 'updated',)


class ItemInstanceAdmin(admin.ModelAdmin):
    exclude = ('slug',)
    list_display = ('id', 'item', 'renter', 'status', 'due_date')


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Format, FormatAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(ItemInstance, ItemInstanceAdmin)
