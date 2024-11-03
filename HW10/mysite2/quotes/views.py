from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegistrationForm, QuoteForm, AuthorForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from .models import Author, Quote, Tag
from django.db.models import Count


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # або ваш код для збереження користувача
            return redirect('some_view')
    else:
        form = UserRegistrationForm()
    return render(request, 'quotes/register.html', {'form': form})


@login_required
def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)
            author = get_object_or_404(Author, id=form.cleaned_data['author'].id)
            quote.author = author
            quote.user = request.user
            quote.save()
            return redirect('quote_list')
    else:
        form = QuoteForm()
    return render(request, 'quotes/add_quote.html', {'form': form})


@login_required
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('author_list')
    else:
        form = AuthorForm()
    return render(request, 'quotes/add_author.html', {'form': form})


def quote_list(request):
    # Отримання всіх цитат
    quotes = Quote.objects.all()

    # Фільтрація за тегами, якщо тег передано в запиті
    tag = request.GET.get('tag')
    if tag:
        quotes = quotes.filter(tags__name__iexact=tag)

    # Пагінація
    paginator = Paginator(quotes, 10)  # 10 цитат на сторінку
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Передача контексту в шаблон
    context = {
        'quotes': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'quotes/quote_list.html', context)


def author_list(request):
    authors = Author.objects.all()
    return render(request, 'quotes/author_list.html', {'authors': authors})


def search_quotes_by_author(request):
    query = request.GET.get('author', '')
    quotes = []
    if query:
        try:
            author = Author.objects.get(name__icontains=query)
            quotes = Quote.objects.filter(author=author).distinct()
        except Author.DoesNotExist:
            quotes = []

    return render(request, 'quotes/search_author_results.html', {'quotes': quotes, 'query': query})


def quotes_by_tag(request, tag_name):
    tag = Tag.objects.get(name=tag_name)
    quotes = Quote.objects.filter(tags=tag).values('text', 'author__name').distinct()
    return render(request, 'quotes/quotes_by_tag.html', {'tag': tag, 'quotes': quotes})


def search_quotes_by_tag(request):
    query = request.GET.get('tag', '')
    quotes = []
    if query:
        try:
            tag = Tag.objects.get(name=query)
            quotes = Quote.objects.filter(tags=tag).distinct()
        except Tag.DoesNotExist:
            quotes = []

    return render(request, 'quotes/search_results.html', {'quotes': quotes, 'query': query})


def quote_detail(request, id):
    quote = get_object_or_404(Quote, id=id)
    return render(request, 'quotes/quote_detail.html', {'quote': quote})


def author_detail(request, id):
    author = get_object_or_404(Author, id=id)
    return render(request, 'quotes/author_detail.html', {'author': author})


@login_required
def edit_quote(request, id):
    quote = get_object_or_404(Quote, id=id)
    if request.method == 'POST':
        form = QuoteForm(request.POST, instance=quote)
        if form.is_valid():
            form.save()
            return redirect('quote_list')
    else:
        form = QuoteForm(instance=quote)
    return render(request, 'quotes/edit_quote.html', {'form': form})


@login_required
def delete_quote(request, id):
    quote = get_object_or_404(Quote, id=id)
    if request.method == 'POST':
        quote.delete()
        return redirect('quote_list')
    return render(request, 'quotes/delete_quote.html', {'quote': quote})


@login_required
def edit_author(request, id):
    author = get_object_or_404(Author, id=id)
    if request.method == 'POST':
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            return redirect('author_list')
    else:
        form = AuthorForm(instance=author)
    return render(request, 'quotes/edit_author.html', {'form': form, 'author': author})


@login_required
def delete_author(request, id):
    author = get_object_or_404(Author, id=id)
    if request.method == 'POST':
        author.delete()
        return redirect('author_list')
    return render(request, 'quotes/delete_author.html', {'author': author})


def home_view(request):
    # Отримуємо топ-10 тегів за кількістю цитат через ManyToMany зв'язок у моделі Quote
    top_tags = Tag.objects.annotate(num_quotes=Count('quote')).order_by('-num_quotes')[:10]

    # Отримуємо останні 5 цитат для відображення
    quotes = Quote.objects.all().order_by('-id')[:5]

    # Поточний рік для відображення у футері
    from datetime import datetime
    current_year = datetime.now().year

    return render(request, 'quotes/home.html', {
        'top_tags': top_tags,
        'quotes': quotes,
        'current_year': current_year,
    })



def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # або інша URL-адреса
    else:
        form = UserCreationForm()
    return render(request, 'quotes/signup.html', {'form': form})


@login_required
def profile_view(request):
    return render(request, 'registration/profile.html', {'user': request.user})
