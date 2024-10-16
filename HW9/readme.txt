# Scrapy Quotes to Scrape Project

## Опис

Цей проєкт здійснює скрапінг сайту [Quotes to Scrape](http://quotes.toscrape.com) за допомогою фреймворку Scrapy. Мета проєкту полягає в тому, щоб зібрати всі цитати та авторів із сайту, зберегти їх у файли `quotes.json` та `authors.json`, а потім завантажити ці дані у хмарну базу даних MongoDB.


## Вимоги

Для цього проекту потрібні наступні бібліотеки:

- Python 3.10+
- Scrapy
- MongoDB
- Mongoengine

Щоб встановити всі залежності, використовуйте Poetry або pip:

```bash
poetry install
# або
pip install -r requirements.txt
