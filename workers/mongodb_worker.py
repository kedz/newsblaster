import os
import sys
from bson import json_util
import json
from datetime import datetime
import yaml
import pymongo

# Import local modules
module_path = os.path.dirname(os.path.realpath(__file__))
messaging_module = os.path.join(module_path,os.path.join('..' + os.sep + 'messaging' ))
sys.path.append(messaging_module)
from messaging_service import Consumer

class MongoDBWorker(object):

	def __init__(self):

		self.module_path = os.path.dirname(os.path.realpath(__file__))
		self.config_dir = os.path.join(self.module_path,os.path.join('..' + os.sep + 'configs' ))
		self.file_path = os.path.abspath(self.config_dir) + os.sep + 'settings.yaml'
 		self.config_file = open(self.file_path,'r')
 		self.config_data = yaml.load(self.config_file)

		self.client = pymongo.MongoClient(self.config_data['mongodb']['host'],self.config_data['mongodb']['port'])
		self.db = self.client[self.config_data['mongodb']['database_name']] 
		self.collection = self.db[self.config_data['mongodb']['article_collection_name']]

	def convert_to_datetime(self,timestamp):
		print timestamp
		date = datetime.fromtimestamp(timestamp/1000)
		print date
		return date

	def handle_delivery(self,channel, method, header, body):

		article = json.loads(body)
		article_id = json_util.loads(article['_id']) 
		article['_id'] = article_id

		article['time_of_crawl'] = self.convert_to_datetime(article['time_of_crawl'])
		if 'date_published' in article['meta_information']:
			article['meta_information']['date_published'] = self.convert_to_datetime(article['meta_information']['date_published'])

		self.collection.update({'_id':article_id},
													  article,
												    True )
    
		channel.basic_ack(delivery_tag = method.delivery_tag)
		print '--Done Inserting To MongoDB--'

	def run(self):
		self.consumer = Consumer('data_distributor',
			      'mongodb_worker',
			      'articles',
			       handle_message=self.handle_delivery)

		self.consumer.start()

if __name__ == "__main__":
	#Starts consumer that just listens to the queue and update messages	
	db_worker = MongoDBWorker()
	db_worker.run()
