from scraper.spiders import moyo_catalog_spider
from scraper.quicksort import QuickSortJson
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


process = CrawlerProcess(get_project_settings())


moyo_laptops = moyo_catalog_spider.MoyoCatalogSpider(name='moyo_laptops')
moyo_laptops.start_urls.append('http://www.moyo.ua/comp-and-periphery/notebooks/?page=1')


process.crawl(moyo_laptops, 'moyo_laptops')
process.start()


key_sort = QuickSortJson('moyo_laptops.json', 'price')
key_sort.sort()
