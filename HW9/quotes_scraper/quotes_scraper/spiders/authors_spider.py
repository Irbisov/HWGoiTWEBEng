import scrapy


class AuthorsSpider(scrapy.Spider):
    name = 'authors_spider'
    start_urls = ['http://quotes.toscrape.com']

    def parse(self, response):
        author_links = response.css('div.quote span a::attr(href)').getall()
        for link in author_links:
            yield response.follow(link, self.parse_author)

        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_author(self, response):
        yield {
            'name': response.css('h3.author-title::text').get().strip(),
            'birthdate': response.css('span.author-born-date::text').get(),
            'bio': response.css('div.author-description::text').get().strip(),
        }
