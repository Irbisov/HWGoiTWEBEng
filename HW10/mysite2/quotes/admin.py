from django.contrib import admin
from .models import Tag, Author, Quote


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'birthdate', 'bio')
    search_fields = ('name',)


class QuoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'author', 'get_tags')
    search_fields = ('text',)
    list_filter = ('author', 'tags')  # Додано фільтрування за тегами

    def get_tags(self, obj):
        """Метод для отримання тегів, асоційованих з цитатою."""
        tags = obj.tags.all()
        return ", ".join(tag.name for tag in tags) if tags else "Без тегів"  # Показуємо "Без тегів", якщо їх немає

    get_tags.short_description = 'Tags'


# Реєстрація моделей в адміністративній панелі
admin.site.register(Tag, TagAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Quote, QuoteAdmin)
