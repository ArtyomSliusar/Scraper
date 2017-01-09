import scrapy
import re
from scraper.items import ScraperMoyo


class MoyoCatalogSpider(scrapy.Spider):
    name = ""
    custom_settings = {
        'ITEM_PIPELINES': {
            'scraper.pipelines.MoyoCleansingPipeline': 301,
            'scraper.pipelines.JsonWriterPipeline': 302,
        }
    }
    start_urls = []

    def parse(self, response):
        last_page = response.xpath('//div[@class="pagination"]//a[last()]//@data-id').extract_first()
        last_page_num = int(last_page)
        i = 1
        while i <= last_page_num:
            url = re.sub(r'page=\d+', r'page={}'.format(i), response.url)
            i += 1
            yield scrapy.Request(url, self.parse_results)

    def parse_results(self, response):
        items = []
        records = response.css('div.goods_item')
        for record in records:
            item = ScraperMoyo()
            item['title'] = record.css('a.goods_title::text').extract_first()
            item['price'] = record.css('div.goodsprice-amount span::text').extract_first()
            item['link'] = record.css('a.goods_image::attr(href)').extract_first()
            items.append(item)
        return items
