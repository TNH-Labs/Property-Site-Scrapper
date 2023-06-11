from django.core.management.base import BaseCommand
from scrapper.spiders.loopnet_spider import LoopNetSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

class Command(BaseCommand):
    help = 'Scrape data from LoopNet'

    def handle(self, *args, **options):
        process = CrawlerProcess(get_project_settings())
        process.crawl(LoopNetSpider)
        process.start()
