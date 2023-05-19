import serial
from time import sleep

angles = [25, 40, -15, 80, -30, 10, 70, 0, -60, 0, -90]

with serial.Serial('COM3',9600,timeout=10) as serial:
    while True:
        try:
            for angle in angles:
                command = str(angle)
                
                serial.write(bytes(command, 'utf-8'))
                data = serial.readline()
                if data:
                    print('Incoming Data:' + data)
                sleep(10)
        except Exception as e:
            print(e)
            serial.close()        
# arduino = serial.Serial('COM3', 9600, timeout=0.5)
# print("connected")
# sleep(5)
# angles = [25, 40, -15, 80, -30, 10, 70, 0, -60, 0, -90]

# for angle in angles:

#     command = str(angle)
#     print(command)
#     arduino.write(bytes(command, 'utf-8'))
#     sleep(10)

# arduino.close()
