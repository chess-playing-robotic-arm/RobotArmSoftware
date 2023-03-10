import pika
from pika.exchange_type import ExchangeType
# from pika.exceptions import AMQPConnectionError
import json
# from time import sleep
# import traceback
import os



EXCHANGE = 'main'

class RabbitMQ():
    def __init__(self,queue,routing_key):
        self.exchange_type = ExchangeType.direct
        self.routing_key = queue
        
        self.url = 'localhost' 
        # self.url = '10.154.7.194'
       
        self.connection_parameters = pika.ConnectionParameters(self.url)
       
        self.connection = pika.BlockingConnection(self.connection_parameters)
        
        print('RabbitMQ Connected')
        self.channel = self.connection.channel()
        self.exchange = self.channel.exchange_declare(
            exchange=EXCHANGE, exchange_type=self.exchange_type)
        
        # self.channel.basic_qos(prefetch_count=1)
        self.queue = self.channel.queue_declare(
            queue=self.routing_key, durable=True)

        
        self.channel.queue_bind(exchange=EXCHANGE,
                                    queue=self.queue.method.queue, routing_key=routing_key)
        

    
        
    def send(self,msg):
        try:
            self.channel.basic_publish(exchange=EXCHANGE, routing_key=self.routing_key, body=msg)
        except Exception as e:
            print(e)
            print(f'Error in Sending {msg}')

    def consume(self,handler):
        def callback(channel, method, properties, body):
            try:
                body = body.decode('UTF-8')
                try:
                    handler(json.loads(body))
                except:
                    handler(body)
            except Exception as e:
                print(f'Error! : Receiving unsuccessful -- {e}')
        
        self.channel.basic_consume(queue=self.routing_key, auto_ack=True,
                                       on_message_callback=callback)
        self.channel.start_consuming()


    def close(self):
        self.connection.close()
        self.connection = None
        self.channel = None
        self.exchange = None