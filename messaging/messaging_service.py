import yaml
import os
import pika

class MessageService(object):

	def __init__(self):
		self.module_path = os.path.dirname(os.path.realpath(__file__))
		self.config_dir = os.path.join(self.module_path,os.path.join('..' + os.sep + 'configs' ))
		self.file_path = os.path.abspath(self.config_dir) + os.sep + 'settings.yaml'
		self.config_file = open(self.file_path,'r')
		self.config_data = yaml.load(self.config_file)
		self.credentials = pika.PlainCredentials(self.config_data['rabbitmq']['username'], self.config_data['rabbitmq']['password'])
		self.connection_parameters = pika.ConnectionParameters(
                                        host=self.config_data['rabbitmq']['host'],
                                        credentials=self.credentials)

class Publisher(MessageService):

	def __init__(self,exchange_name):
		self.channel = None
		self.exchange_name = exchange_name
		super(Publisher,self).__init__()



	def send_message(self,message,routing_key):
		
		self.connection = pika.BlockingConnection(parameters=self.connection_parameters)

		self.channel = self.connection.channel()

		self.channel.basic_publish(exchange=self.exchange_name,
                      routing_key=routing_key,
                      body=message,
                      properties=pika.BasicProperties(delivery_mode =2,))

	def close_connection(self):
		self.connection.close()


class Consumer(MessageService):

  def __init__(self,exchange_name):
    self.channel = None
    self.exchange_name = exchange_name
    super(Consumer,self).__init__()

	
	#TODO complete after datababse is up


