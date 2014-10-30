#!/usr/bin/env python
import pika
import sys
import os
import yaml
from pprint import pprint
import pymongo
from pymongo import MongoClient
import json

module_path = os.path.dirname(os.path.realpath(__file__))
config_dir = os.path.join(module_path, os.path.join('..' + os.sep + 'configs'))
file_path = os.path.abspath(config_dir) + os.sep + 'ronas_settings.yaml'
config_file = open(file_path, 'r')
config_data = yaml.load(config_file)

client = MongoClient()

credentials = pika.PlainCredentials(config_data['rabbitmq']['username'],
                                    config_data['rabbitmq']['password'])

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=config_data['rabbitmq']['host'],
    credentials=credentials))

channel = connection.channel()

channel.queue_declare(queue='database_queue', durable=True)

json_to_string = json.dumps({'Test1': 'this could be an new article'})

print channel.basic_publish(exchange='',
                            routing_key='database_queue',
                            body=json_to_string)

print "--Sent--"
connection.close()
