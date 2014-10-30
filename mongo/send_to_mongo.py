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

print ' [*] Waiting for messages. To exit press CTRL+C'


def callback(ch, method, properties, body):
    client = MongoClient()
    db = client['test']
    collection = db.test_collection
    dictionary = json.loads(body)
    collection.insert(dictionary)
    print " [x] Received %r" % (body)

channel.basic_consume(callback,
                      queue='database_queue',
                      no_ack=True)

channel.start_consuming()
