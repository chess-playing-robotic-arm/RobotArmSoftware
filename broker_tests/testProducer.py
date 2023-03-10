from datetime import datetime

import sys
sys.path.insert(0,"..")

from message_broker.broker import RabbitMQ
import time
import json


producer = RabbitMQ('fen','fen')
fen_lst = ['3nr3/7k/1BP5/8/1Ppp2b1/1P1pqr2/K5Pp/8 w - - 0 1',
           '1N5b/8/2P1P3/3K1p2/R2B2b1/1P1p4/1Pkn3p/r7 w - - 0 1',
           '1Q6/3P1RR1/4q3/P4p2/1P2r3/1n1kP3/P3p2K/5b2 w - - 0 1',
           '5B2/pP3k2/Q1q5/2P5/P5P1/Ppp1p2N/8/1K3B2 w - - 0 1',
           '1B2n3/3n4/Np4bR/7B/2r3p1/K3P3/p3p3/4k2q w - - 0 1',
           '7B/8/3PR3/1p3k2/nP5p/2P1PN1p/1P2b3/4K2N w - - 0 1',
           'n3k3/4p1P1/1BP1B2p/5K1P/4p3/2P3pP/4r2p/8 w - - 0 1',
           '8/2p2p1r/P1p1N3/3kr2P/2p5/1p3P2/P2B3P/5K2 w - - 0 1',
           ]

x = 0
#? msg structure: {
#? "fen":'3nr3/7k/1BP5/8/1Ppp2b1/1P1pqr2/K5Pp/8 w - - 0 1',
#? "time":'10-03-23-10:55'
#? }
while True:
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    msg = {"fen":fen_lst[x],"time":current_time}
    producer.send(json.dumps(msg))
    print(f'{fen_lst[x]} send')
    time.sleep(2)
    x += 1
    if(x == len(fen_lst)): x = 0
