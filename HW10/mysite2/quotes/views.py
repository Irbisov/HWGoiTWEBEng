from datetime import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import UserRegistrationForm, QuoteForm, AuthorForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from .models import Author, Quote


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
    quotes = Quote.objects.all()
    return render(request, 'quotes/quote_list.html', {'quotes': quotes})


def author_list(request):
    authors = Author.objects.all()
    return render(request, 'quotes/author_list.html', {'authors': authors})


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
    quotes = Quote.objects.all()
    return render(request, 'quotes/home.html', {'quotes': quotes, 'current_year': datetime.now().year})


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
