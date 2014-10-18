import os
import sys
import json
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

	def handle_delivery(self,channel, method, header, body):

	
		article = json.loads(body) 
		#TODO correctly deserialize _id and all date fields to the correct Python class	
	
		self.collection.update({'_id':article['_id']},
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
