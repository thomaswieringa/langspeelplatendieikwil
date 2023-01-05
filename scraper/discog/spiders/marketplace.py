import scrapy
from scrapy.selector import Selector
import re

from ..google_sheet_reader import get_sheet
from ..discogs_versions import DiscogsVersions


def separate_currency(string):
    print('string:{}'.format(string))
    # we remove any + signs
    string = string.replace("+", "")
    # Use a regular expression to extract the currency sign and the amount
    match = re.search(r'([^\d^\.]+)(\d+\.\d+)', string)
    if not match:
        if 'no extra shipping' in string:
            return 0, 'FREE'
        else:
            return string, ""

    # Extract the currency sign and the amount
    currency_sign = match.group(1)
    amount = float(match.group(2))
    # Map the currency sign to the corresponding ISO code
    currency_mapping = {
        '$': 'USD',
        '€': 'EUR',
        '£': 'GBP',
        '¥': 'JPY',
        'CA$': 'CAD',
        'A$': "AUD"
    }
    print('currency_sign:{}'.format(currency_sign))
    if currency_sign not in currency_mapping:
        return amount, currency_sign
    currency_code = currency_mapping[currency_sign]

    return amount, currency_code


class MarketPlaceSpider(scrapy.Spider):
    name = 'marketplace'
    allowed_domains = ['www.discogs.com']

    def start_requests(self):
        # we load the master id'd from sheets
        master_df = get_sheet()
        # then we initialize the discogs class to be able to get all versions
        discogs_versions = DiscogsVersions(key="IjDxhwugeqUVGtMZuJZQqCazFHdMQXKrZOTesFTj",
                            user="thomaswieringa")
        print('master df')
        print(master_df)
        for master_id in master_df['master_id']:
            for release_id in discogs_versions.all_versions(master_id):
                print('searching release id: {}'.format(release_id['id']))
                yield scrapy.Request('https://www.discogs.com/sell/release/{}?sort=price%2Casc&limit=250&ev=rb&page=1'
                                     .format(release_id['id']),
                                     cb_kwargs={'master_id': master_id, 'release_id': release_id['id']})

    def parse(self, response, master_id, release_id):
        records = response.xpath('//tbody/tr').getall()
        for listing in records:
            available = Selector(text=listing).xpath('//a[@class="button button-green cart-button "]').get() is not None
            item = {
                'title': Selector(text=listing).xpath('body/tr/td[2]/strong/a/text()').get().strip(),
                'release_id': release_id,
                'master_id': master_id,
                'link': Selector(text=listing).xpath('body/tr/td[2]/strong/a/@href').get().strip(),
                'media_condition': Selector(text=listing).xpath('//p[@class="item_condition"]/span[3]/text()').get().strip(),
                'sleeve_condition': Selector(text=listing).xpath('//span[@class="item_sleeve_condition"]/text()').get().strip(),
                'seller': Selector(text=listing).xpath('body/tr/td[3]/ul/li[1]/div/strong/a/text()').get().strip(),
                'seller_link': Selector(text=listing).xpath('body/tr/td[3]/ul/li[1]/div/strong/a/@href').get().strip(),
                'ships_from': Selector(text=listing).xpath('body/tr/td[3]/ul/li[3]/text()').get().strip(),
                'price': separate_currency(Selector(text=listing).xpath('body/tr/td[5]/span[1]/text()').get().strip())[0],
                'price_currency': separate_currency(Selector(text=listing).xpath('body/tr/td[5]/span[1]/text()').get().strip())[1],
                'shipping': separate_currency(Selector(text=listing).xpath('body/tr/td[5]/span[2]/text()').get().strip())[0],
                'shipping_currency': separate_currency(Selector(text=listing).xpath('body/tr/td[5]/span[2]/text()').get().strip())[1],
                'available': int(available)
            }
            yield item
        # todo: implement scraping next page functionality. Not really needed since a page contains 250 items.
        # item_sleeve_condition
        # next_page = response.css('').get()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)


