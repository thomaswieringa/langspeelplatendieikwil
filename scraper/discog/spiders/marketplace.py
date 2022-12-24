import scrapy
from scrapy.selector import Selector


class MarketPlaceSpider(scrapy.Spider):
    name = 'marketplace'
    allowed_domains = ['www.discogs.com']

    def start_requests(self):
        yield scrapy.Request('https://www.discogs.com/sell/release/{}?sort=price%2Casc&limit=250&ev=rb&page=1'
                             .format(self.release_id))
        # yield scrapy.Request('https://www.discogs.com/sell/list?sort=listed%2Cdesc&limit=250&q={}&page=1'
        #                      .format(self.release_id))

    def parse(self, response):
        records = response.xpath('//tbody/tr').getall()
        for listing in records:
            item = {
                'title': Selector(text=listing).xpath('body/tr/td[2]/strong/a/text()').get().strip(),
                'release_id': self.release_id,
                'master_id': self.master_id,
                'link': Selector(text=listing).xpath('body/tr/td[2]/strong/a/@href').get().strip(),
                'media_condition': Selector(text=listing).xpath('//p[@class="item_condition"]/span[3]/text()').get().strip(),
                'sleeve_condition': Selector(text=listing).xpath('//span[@class="item_sleeve_condition"]/text()').get().strip(),
                'seller': Selector(text=listing).xpath('body/tr/td[3]/ul/li[1]/div/strong/a/text()').get().strip(),
                'seller_link': Selector(text=listing).xpath('body/tr/td[3]/ul/li[1]/div/strong/a/@href').get().strip(),
                'price': Selector(text=listing).xpath('body/tr/td[5]/span[1]/text()').get().strip(),
                'shipping': Selector(text=listing).xpath('body/tr/td[5]/span[2]/text()').get().strip(),
            }
            yield item
        # todo: implement scraping next page functionality. Not really needed since a page contains 250 items.
        # item_sleeve_condition
        # next_page = response.css('').get()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)
