# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import pyodbc


class AzureSQLPipeline:

    def __init__(self, connection_string, username, password):
        self.conn = None
        self.cursor = None
        self.connection_string = connection_string
        self.username = username
        self.password = password

    def open_spider(self, spider):
        server = 'discog-scrapes.database.windows.net'
        database = 'discogs-scrapes'
        username = 'thomas'
        password = 'Wiering@1'
        driver = '{ODBC Driver 17 for SQL Server}'
        self.conn = pyodbc.connect('DRIVER='+driver+';'
                                                    'SERVER=tcp:'+server+
                                   ';PORT=1433;DATABASE='+database+';'
                                                                   'UID='+username+';PWD='
                                   + password)
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        # Insert the item into the database
        self.cursor.execute(
            "INSERT INTO table_name (column1, column2, column3) VALUES (?, ?, ?)",
            (item['field1'], item['field2'], item['field3'])
        )
        self.conn.commit()
        return item