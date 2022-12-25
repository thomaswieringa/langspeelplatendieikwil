# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import pyodbc


class AzureSQLPipeline:


    def open_spider(self, spider):
        server = 'discog-scrapes.database.windows.net'
        database = 'discogs-scrapes'
        username = 'thomas'
        password = 'Wiering@1'
        driver = '{ODBC Driver 17 for SQL Server}'
        self.conn = pyodbc.connect('DRIVER=' + driver + ';'
                                                        'SERVER=tcp:' + server +
                                   ';PORT=1433;DATABASE=' + database + ';'
                                                                       'UID=' + username + ';PWD='
                                   + password)
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        # Insert the item into the database
        self.cursor.execute(
            "INSERT INTO MarketPlace  VALUES (?, ?, ?)",
            (item['release_id'], item['master_id'], item['link'],
             item['media_condition'], item['sleeve_condition'], item['seller'],
             item['seller_link'], item['price'], item['price_currency'],
             item['shipping'], item['shipping_currency'])
        )
        self.conn.commit()
        return item