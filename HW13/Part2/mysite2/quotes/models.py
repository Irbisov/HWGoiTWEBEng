from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    """Модель для авторів."""
    name = models.CharField(max_length=255, unique=True)
    bio = models.TextField(blank=True, default='NEW')
    birthdate = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Модель для тегів."""
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Quote(models.Model):
    text = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)  # Поле, яке ви хочете фільтрувати

    def __str__(self):
        return f"{self.text[:50]}... - {self.author.name}"  # Повертає перші 50 символів цитати


class QuoteTag(models.Model):
    """Модель для зв'язку цитат з тегами."""
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name='quote_tags')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='tagged_quotes')

    class Meta:
        unique_together = ('quote', 'tag')  # Уникати дублікатів у зв'язках

    def __str__(self):
        return f"{self.quote.text[:50]}... tagged with {self.tag.name}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Зв'язок з користувачем
    avatar = models.ImageField(upload_to='avatars/', default='default_avatar.png')  # Аватар профілю

    def __str__(self):
        return f'Profile for {self.user.username}'
