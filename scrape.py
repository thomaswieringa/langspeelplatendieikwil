# this script deletes the Offers from database and runs the scrapy scraper
# to fill it again
import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'backend.backend.settings'
django.setup()
from django.contrib.auth.models import User
from api.models import Offer, Master

os.environ['SCRAPY_SETTINGS_MODULE'] = 'scraper.discog.settings'
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scraper.discog.spiders.marketplace import MarketPlaceSpider


USER_ID = 2
user = User.objects.get(id=USER_ID)
Offer.objects.filter(user=user).delete()

masters = Master.objects.filter(user=user)

process = CrawlerProcess(get_project_settings())
process.crawl(MarketPlaceSpider, masters=masters)
process.start()

