This module is used  to abstract the internals of messaging  from other components that require it in NewsBlaster. 

----------
Usage Example
-------------

**Publisher**

Used to send messages with a specific routing key to an exchange on the broker. The queue name does not have to be known in advance. 

Parameters:

- exchange_name - Name of the exchange on the broker  
- routing_key - The    routing key that will be used to deliver your messages to specific    queues based on bindings  
- payload - The  "stuff" you want to send




        from messaging_service import Publisher
        publisher = Publisher('exchange_name')
        publisher.send_message('payload','routing_key')




**Consumer**

Parameters:

- exchange_name - Name of the exchange on the broker  
- routing_key - The    routing key that will be used to deliver your messages to specific    queues based on bindings  
- payload - The  "stuff" you want to send

Additionally you need to provide a method with the signature below to handle deliveries of messages for your consumer. `handle_deliver(.....)`

from messaging_service import Consumer
import json
    
    def handle_delivery(self,channel, method, header, body):
    
      message =  json.loads(body)
     #Determine what you would like to to do with the received message
      
      channel.basic_ack(delivery_tag = method.delivery_tag)
     
      consumer = Consumer('data_distributor',
                             'annotator_worker',
                             'articles',
                             handle_message=handle_delivery)


> [RabbitMQ](http://www.rabbitmq.com/).


