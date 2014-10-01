#!/usr/bin/env python
import pika
import sys
import os
import yaml
from pprint import pprint

module_path = os.path.dirname(os.path.realpath(__file__))
config_dir = os.path.join(module_path,os.path.join('..' + os.sep + 'configs' ))
file_path = os.path.abspath(config_dir) + os.sep + 'settings.yaml'
config_file = open(file_path,'r')
config_data = yaml.load(config_file)

credentials = pika.PlainCredentials(config_data['rabbitmq']['username'] , config_data['rabbitmq']['password'])

connection = pika.BlockingConnection(pika.ConnectionParameters(
                          host=config_data['rabbitmq']['host'],
                          credentials=credentials))

channel = connection.channel()

#Declares the entry exchange to be used by all producers to send messages. Could be external producers as well
channel.exchange_declare(exchange='data_gateway',
      exchange_type='fanout',
      durable=True,
      auto_delete=False)

#Declares the processing exchange to be used.Routes messages to various queues. For internal use only
channel.exchange_declare(exchange='data_distributor',
      exchange_type='topic',
      durable=True,
      auto_delete=False)

#Binds the external/producer facing exchange to the internal exchange
channel.exchange_bind(destination='data_distributor',source='data_gateway')

##Create Durable Queues binded to the data_distributor exchange
channel.queue_declare(queue='database_queue',durable=True)

#Bind queues to exchanges and correct routing key. Allows for messages to be saved when no consumer is present
channel.queue_bind(queue='database_queue',exchange='data_distributor',routing_key='articles')
