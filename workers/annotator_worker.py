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
from messaging_service import Publisher

class AnnotatorWorker(object):

	def __init__(self):
		pass

	def send_to_broker(self,annotated_article):
		publisher = Publisher('data_distributor')
		publisher.send_message(annotated_article,'articles')

	def handle_delivery(self,channel, method, header, body):

		article = json.loads(body)

		#1.TODO All annotator work would ideally be done here. Import annotator module being developed
		#2.TODO  Once the article that was sent is annotated. Send it back to be saved to the database 

		annotated_article = json.dumps('new article here')
		self.send_to_broker(annotated_article)

 		channel.basic_ack(delivery_tag = method.delivery_tag)
		print '--Done Annotating Article--'


	def run(self):	
		self.consumer = Consumer('data_distributor',
            'annotator_worker',
            'articles',
             handle_message=self.handle_delivery)

		self.consumer.start()		


if __name__ == "__main__":
        #Starts consumer that just listens to the queue and update messages
        ann_worker = AnnotatorWorker()
        ann_worker.run()
