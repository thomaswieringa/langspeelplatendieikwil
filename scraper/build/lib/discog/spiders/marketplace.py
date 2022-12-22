import scrapy
from scrapy.selector import Selector


class ReleaseScraperSpider(scrapy.Spider):
    name = 'marketplace'
    allowed_domains = ['www.discogs.com']

    def start_requests(self):
        yield scrapy.Request('https://www.discogs.com/sell/list?sort=listed%2Cdesc&limit=250&q={}&page=1'
                             .format(self.release_id))

    def parse(self, response):
        records = response.xpath('//tbody/tr').getall()
        for listing in records:
            item = {
                'title': Selector(text=listing).xpath('body/tr/td[2]/strong/a/text()').get(),
                'release_id': self.release_id,
                'link': Selector(text=listing).xpath('body/tr/td[2]/strong/a/@href').get(),
                'media_condition': Selector(text=listing).xpath('//p[@class="item_condition"]/span[3]/text()').get(),
                'sleeve_condition': Selector(text=listing).xpath('//span[@class="item_sleeve_condition"]/text()').get(),
                'seller': Selector(text=listing).xpath('body/tr/td[3]/ul/li[1]/div/strong/a/text()').get(),
                'seller_link': Selector(text=listing).xpath('body/tr/td[3]/ul/li[1]/div/strong/a/@href').get(),
                'price': Selector(text=listing).xpath('body/tr/td[5]/span[1]/text()').get(),
                'shipping': Selector(text=listing).xpath('body/tr/td[5]/span[2]/text()').get(),
            }
            yield item
        # todo: implement scraping next page functionality. Not really needed since a page contains 250 items.
        # item_sleeve_condition
        # next_page = response.css('').get()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)
