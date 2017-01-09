import scrapy
import re
from scrapy_splash import SplashRequest
from scraper.items import ScraperRozetka


class RozetkaCatalogSpider(scrapy.Spider):
    name = ""
    start_urls = []

    def parse(self, response):
        last_page = response.xpath('//ul[@name="paginator"]//li[last()]//@id').extract_first()
        last_page_num = int(last_page[-1])
        i = 1
        while i <= last_page_num:
            url = re.sub(r'page=\d+', r'page={}'.format(i), response.url)
            i += 1
            yield SplashRequest(url, self.parse_results, endpoint='render.html', args={'wait': 0.5, 'timeout': 60})

    def parse_results(self, response):
        items = []
        records = response.css('div.g-i-tile-catalog')
        for record in records:
            item = ScraperRozetka()
            item['title'] = record.css('img::attr(title)').extract_first()
            item['price'] = record.css('div.g-price-uah::text').extract_first()
            item['link'] = record.css('div.g-i-tile-i-title a::attr(href)').extract_first()
            items.append(item)
        return items
