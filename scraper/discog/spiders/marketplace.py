import scrapy
from scrapy.selector import Selector
import re


def separate_currency(string):
    # Use a regular expression to extract the currency sign and the amount
    match = re.search(r'([^\d^\.]+)(\d+\.\d+)', string)
    if not match:
        raise ValueError("Invalid currency string")

    # Extract the currency sign and the amount
    currency_sign = match.group(1)
    amount = float(match.group(2))

    # Map the currency sign to the corresponding ISO code
    currency_mapping = {
        '$': 'USD',
        '€': 'EUR',
        '£': 'GBP',
        '¥': 'JPY'
    }
    if currency_sign not in currency_mapping:
        raise ValueError("Unsupported currency")
    currency_code = currency_mapping[currency_sign]

    return amount, currency_code


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
                'price': separate_currency(Selector(text=listing).xpath('body/tr/td[5]/span[1]/text()').get().strip())[0],
                'price_currency': separate_currency(Selector(text=listing).xpath('body/tr/td[5]/span[1]/text()').get().strip())[1],
                'shipping': separate_currency(Selector(text=listing).xpath('body/tr/td[5]/span[2]/text()').get().strip())[0],
                'shipping_currency':separate_currency(Selector(text=listing).xpath('body/tr/td[5]/span[2]/text()').get().strip())[1],
            }
            yield item
        # todo: implement scraping next page functionality. Not really needed since a page contains 250 items.
        # item_sleeve_condition
        # next_page = response.css('').get()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)

    import re

