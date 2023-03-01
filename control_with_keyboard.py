import threading
import serial 
import keyboard
# import time

global right_pos
global left_pos 
global base_pos
global arm_pos 
global arm_state 
global motor 

def keyboard_input_thread(callback):
 
  
  def keyboard_input():
   
    while True:
      # Wait for user input
      c = keyboard.read_key()
      if c == 'esc':
        exit()
      elif c == 'd' or c == 'a' or c == 'w' or c == 's' or c == 'right' or c == 'left' or c == 'space':
        print(c)
        callback(c)
    
    #   elif c == 'a':
    #     pos_x -= 1
    #     callback(pos_x,0)
    #     print(pos_x)
    #   elif c == 'right':
    #     pos_y += 1
    #     callback(pos_y,1)
    #     print(pos_y)
    #   elif c == 'left':
    #     pos_y -= 1
    #     callback(pos_y,1)
    #     print(pos_y)

      else:
        print(c + ' is Pressed')
        print('Nothing Happened')
  thread = threading.Thread(target=keyboard_input)
  thread.start()


def main():
    
    arduino = serial.Serial('COM3', 9600, timeout=0.1)

    def sendToArduino(key):       
        try:
            # time.sleep(5)
            print(str(motor))
            if(key == 'w'):
                print('www')
                left_pos += 1
                motor = 1
                command = str(motor) + str(left_pos) + '|'
                print(command)
                # arduino.write(str(command).encode())
            elif(key == 's'):
                left_pos -=1
                motor = 1
                command = str(motor) + str(left_pos) + '|'
                print(command)
                # arduino.write(str(command).encode())
            elif(key == 'd'):
                right_pos += 1
                motor = 0
                command = str(motor) + str(right_pos) + '|'
                print(command)
                # arduino.write(str(command).encode())
            elif(key == 'a'):
                right_pos -= 1
                motor = 0
                command = str(motor) + str(right_pos) + '|'
                print(command)
                # arduino.write(str(command).encode())
            elif(key == 'right'):
                base_pos += 1
                motor = 2
                command = str(motor) + str(base_pos) + '|'
                print(command)
                # arduino.write(str(command).encode())
            elif(key == 'left'):
                base_pos -1
                motor = 2
                command = str(motor) + str(base_pos) + '|'
                print(command)
                # arduino.write(str(command).encode())
            elif(key == 'space'):
                # toggle_arm()
                motor = 3
                command = str(motor) + str(arm_pos) + '|'
                print(command)
                # arduino.write(str(command).encode())



            # command = str(motor) + str(pos) + '|'
            arduino.write(str(command).encode())
            # data = arduino.readline()
            # if data:
            #     print(data)
            #     print('Hi Arduino')
        except:
            # print('exception')
            arduino.close()

    keyboard_input_thread(sendToArduino)
    

right_pos = 20
left_pos = 40
base_pos = 90
arm_pos = 120
arm_state = True
motor = 0


main()