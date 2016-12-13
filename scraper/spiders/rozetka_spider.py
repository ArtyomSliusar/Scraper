import scrapy
import re
from scrapy_splash import SplashRequest
from scraper.items import ScraperRozetka


class RozetkaSpider(scrapy.Spider):
    name = "laptops"
    start_urls = [
        'http://rozetka.com.ua/notebooks/c80004/filter/producer=dell;page=1/',
        'http://rozetka.com.ua/notebooks/c80004/filter/producer=lenovo;page=1/',
    ]

    def parse(self, response):
        paginator = response.xpath('//ul[@name="paginator"]//li')
        page_count = len(paginator)

        for i in range(1, page_count+1):
            url = re.sub(r'page=\d+', r'page={}'.format(i), response.url)
            yield SplashRequest(url, self.parse_results, endpoint='render.html', args={'wait': 0.5})

    def parse_results(self, response):
        items = []
        for record in response.css('div.g-i-tile-catalog'):
            item = ScraperRozetka()
            item['title'] = record.css('img::attr(title)').extract_first()
            item['price'] = record.css('div.g-price-uah::text').extract_first()
            item['link'] = record.css('div.g-i-tile-i-title a::attr(href)').extract_first()
            items.append(item)
        return(items)


