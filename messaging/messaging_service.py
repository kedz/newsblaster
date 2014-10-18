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

	def __init__(self,exchange_name,queue_name,routing_key,handle_message=None):
		self.exchange_name = exchange_name
		self.queue_name = queue_name
		self.routing_key = routing_key
		self.channel = None

		#Override the handle message for consumer
		if handle_message:
			self.handle_delivery=handle_message

		super(Consumer,self).__init__()

		self.connection = pika.SelectConnection(self.connection_parameters, self.on_connected)

	def on_connected(self,connection):
		"""Called when we are fully connected to RabbitMQ"""
		# Open a channel
		self.connection.channel(self.on_channel_open)

	def on_channel_open(self,new_channel):
		"""Called when our channel has opened"""
		self.channel = new_channel
		
		#Not required if queues are already configured
		self.channel.queue_declare(queue=self.queue_name, 
															durable=True, 
															exclusive=False, 
															auto_delete=False, 
															callback=self.on_queue_declared)

		self.channel.queue_bind(callback=self.on_queue_declared,
		exchange=self.exchange_name,
		queue=self.queue_name,
		routing_key=self.routing_key)

	def on_queue_declared(self,frame):
		"""Called when RabbitMQ has told us our Queue has been declared, frame is the response from RabbitMQ"""
		self.channel.basic_consume(self.handle_delivery , queue=self.queue_name)


	def handle_delivery(self,channel, method, header, body):
		"""Called when we receive a message from RabbitMQ"""
		print body
		channel.basic_ack(delivery_tag = method.delivery_tag)
 		print 'done processing message. Over write for each consumer'

	def start(self):
		try:
			#Continually listen for messages on  RabbitMQ
			self.connection.ioloop.start()
		except KeyboardInterrupt:
		# Gracefully close the connection
			selfconnection.close()
			# Loop until we're fully closed, will stop on its own
			self.connection.ioloop.start()


