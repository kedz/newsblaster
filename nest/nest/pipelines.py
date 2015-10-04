import os
import sys
from twisted.internet.threads import deferToThread

# Import local modules
module_path = os.path.dirname(os.path.realpath(__file__))

datastore_module = os.path.join(module_path,os.path.join('..' + os.sep + '..' + os.sep + 'datastore' ))
sys.path.append(datastore_module)
from mongo import MongoStore


# Define your item pipelines here
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

class SendToDataStorePipeline(object):

    def __init__(self):
        self.db = MongoStore()

    def process_item(self, item, spider):
    #Runs saving to db separate thread to prevent it from blocking
    #on single items
        return deferToThread(self._process_item, item, spider)

    def _process_item(self, item, spider):

        item_dict = dict(item)
        self.db.insert_article(item)
        return item

class ArticleEnrichmentPipeLine(object):

    def process_item(self,item,spider):
    #1. We mentioned in the meeting that there are some other libraries
    #   that will help in extracting meta information. Those libraries
    #   can be inported and used here by updating the item  
        return item


class ArticleSummarizationPipeline(object):

    def process_item(self, item, spider):
        #Summarize articles here 
        return item
