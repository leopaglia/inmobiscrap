# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


class MongoPipeline(object):

    client = None

    def __init__(self, host, port, db, col):
        self.host = host
        self.port = port
        self.db = db
        self.col = col

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MONGO_HOST'),
            port=crawler.settings.get('MONGO_PORT'),
            db=crawler.settings.get('MONGO_DB'),
            col=crawler.settings.get('MONGO_COL')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.host, self.port)

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # insert if not found by address, else update
        query = {'address': dict(item).get('address')}
        self.client[self.db][self.col].update(query, dict(item), upsert=True)
        return item
