from datetime import datetime

import sys
sys.path.insert(0,"..")

from message_broker.broker import RabbitMQ

consumer = RabbitMQ('bestMove')


def handler(msg):
    print(f'BestMove is : {msg}')
    
    

consumer.consume(handler=handler)