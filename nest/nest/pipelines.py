import os
import sys
from twisted.internet.threads import deferToThread
from scrapy.utils.serialize import ScrapyJSONEncoder
from bson.objectid import ObjectId
from bson.json_util import dumps

# Import local modules
module_path = os.path.dirname(os.path.realpath(__file__))
messaging_module = os.path.join(module_path,os.path.join('..' + os.sep + '..' + os.sep + 'messaging' ))
sys.path.append(messaging_module)
from messaging_service import Publisher

# Define your item pipelines here
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

class SendToBrokerPipeline(object):

	def __init__(self):
		self.publisher = Publisher('data_distributor')
		self.encoder = ScrapyJSONEncoder()
	

	def process_item(self, item, spider):
		#Runs sending broker in separate thread to prevent it from blocking
		#on single items
		return deferToThread(self._process_item, item, spider)

	def _process_item(self, item, spider):

		item_dict = dict(item)

		data = self.encoder.encode(item_dict)
		self.publisher.send_message(data,'articles')
		return item

class ArticleEnrichmentPipeLine(object):
	
	def process_item(self,item,spider):
		#1. We mentioned in the meeting that there are some other libraries
    #   that will help in extracting meta information. Those libraries
    #   can be inported and used here by updating the item  
		return item


class ArticleTextExtractionPipeline(object):

	def process_item(self, item, spider):
		#Extract text from html for each broker here 
		return item
