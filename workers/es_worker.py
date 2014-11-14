import os
import sys
from bson import json_util
import json
from datetime import datetime
import yaml
from elasticsearch import Elasticsearch

# Import local modules
module_path = os.path.dirname(os.path.realpath(__file__))
messaging_module = os.path.join(module_path,os.path.join('..' + os.sep + 'messaging' ))
sys.path.append(messaging_module)
from messaging_service import Consumer

class ElasticSearchWorker(object):

	def __init__(self):

		self.module_path = os.path.dirname(os.path.realpath(__file__))
		self.config_dir = os.path.join(self.module_path,os.path.join('..' + os.sep + 'configs' ))
		self.file_path = os.path.abspath(self.config_dir) + os.sep + 'settings.yaml'
 		self.config_file = open(self.file_path,'r')
 		self.config_data = yaml.load(self.config_file)

		#Should ideally read from config file	
		self.es = Elasticsearch()


	def convert_to_datetime(self,timestamp):
		date = datetime.fromtimestamp(timestamp/1000)
		return date

	def handle_delivery(self,channel, method, header, body):

		article = json.loads(body)
		article['time_of_crawl'] = self.convert_to_datetime(article['time_of_crawl'])
		if 'date_published' in article['meta_information']:
			article['meta_information']['date_published'] = self.convert_to_datetime(article['meta_information']['date_published'])


		es_result = self.es.index(index="news", doc_type="article", body=article)
		self.es.indices.refresh(index="news")

		channel.basic_ack(delivery_tag = method.delivery_tag)
		print '--Done Inserting To ElasticSearch--'


	def run(self):
		self.consumer = Consumer('data_distributor',
			      'elasticsearch_worker',
			      'articles',
			       handle_message=self.handle_delivery)

		self.consumer.start()

if __name__ == "__main__":
	#Starts consumer that just listens to the queue and update messages	
	es_worker = ElasticSearchWorker()
	es_worker.run()
