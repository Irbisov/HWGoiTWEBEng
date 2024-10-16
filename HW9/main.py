from scrapy.crawler import CrawlerProcess
from quotes_scraper.quotes_scraper.spiders.quotes_spider import QuotesSpider
from quotes_scraper.quotes_scraper.spiders.authors_spider import AuthorsSpider

# Ініціалізація процесу Scrapy
process = CrawlerProcess()

# Додаємо пауків
process.crawl(QuotesSpider)
process.crawl(AuthorsSpider)

# Запуск
process.start()
