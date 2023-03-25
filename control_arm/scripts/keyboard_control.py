import threading
import serial 
import keyboard
import json
import time

#! find the arduino code or write again.
#! smooth the movement of the arm.
#! improve this code adding functionalities for moving up and down directly. 

# TODO : format this file and restructure !! 

def keyboard_input_thread(callback,saveToFile,makeMove):
  
  def keyboard_input():
    r_movements = []
    l_movements = []
    b_movements = []
    a_movements = []
    movements = []
    is_recording = False
    right_pos = 40
    left_pos = 60
    base_pos = 145
    arm_pos = 120

    while True:
      # Wait for user input
      c = keyboard.read_key()
      if c == 'esc':
        exit()
      elif c == 'w':
        left_pos += 1
        callback(left_pos,1)
        if is_recording : l_movements.append(left_pos)
        
      elif c == 's':
        left_pos -= 1
        callback(left_pos,1)
        if is_recording : l_movements.append(left_pos)
        
      elif c == 'd':
        right_pos += 1
        callback(right_pos,0)
        if is_recording : r_movements.append(right_pos)
       
      elif c == 'a':
        right_pos -= 1
        callback(right_pos,0)
        if is_recording : r_movements.append(right_pos)
        
      elif c == 'right':
        base_pos += 1
        callback(base_pos,2)
        if is_recording : b_movements.append(base_pos)
        
      elif c == 'left':
        base_pos -= 1
        callback(base_pos,2)
        if is_recording : b_movements.append(base_pos)

      elif c == 'space':
        arm_pos += 20
        callback(arm_pos,3)
        if is_recording : a_movements.append(arm_pos)
        
      elif c == 'v':
        arm_pos -= 20
        callback(arm_pos,3)
        if is_recording : a_movements.append(arm_pos)
      
      elif c == 'r':
        if(not is_recording):
          is_recording = True
          print('Recording Started ...')
          print('press u to save')
      
      elif c == 'u':
        is_recording = False
        saveToFile(r_movements,l_movements,b_movements,a_movements,movements)
        print('Saving ...')

      elif c == 'm':
        print('Trying to play e2 to e4............')
        makeMove('e2','e4')
      
      else:
        # print(c + ' is Pressed')
        print('Nothing Happened')
      
      if(is_recording):  
        movements.append({'r': right_pos,'l':left_pos,'b':base_pos,'a':arm_pos})
      
  thread = threading.Thread(target=keyboard_input)
  thread.start()


def main():
    arduino = serial.Serial('COM3', 9600, timeout=0.1)
    moves = {'o':[16,48,145],'e2': [65,74,111],'e4':[61,72,97]}
    
    arduino.write('160|'.encode())
    time.sleep(1)
    arduino.write('040|'.encode())
    time.sleep(1)
    arduino.write('290|'.encode())
    time.sleep(1)
    arduino.write('3125|'.encode())
    
    

    def sendToArduino(pos,motor):       
        try:
            # time.sleep(5)
            
            command = str(motor) + str(pos) + '|'
            print('Motor : ' + str(motor) + ' Angle : ' + str(pos))
            arduino.write(str(command).encode())
            # data = arduino.readline()
            # if data:
            #     print(data)
            #     print('Hi Arduino')
        except:
            arduino.close()
            
    def saveToFile(r_movements,l_movements,b_movements,a_movements,total_movements):
      r_str = ','.join(map(str, r_movements))
      l_str = ','.join(map(str, l_movements))
      b_str = ','.join(map(str, b_movements))
      a_str = ','.join(map(str, a_movements))
      # Open the file in write mode
      with open("./outputs/movements_recorded.txt", "w") as file:
        # Write the string to the file
        file.writelines('Right Motor : \n')
        file.writelines(str(r_movements[0]) + ',' + str(r_movements[-1]) + '\n')
        file.write(r_str)
        file.writelines('\n***********************************************\n')
        file.writelines('Left Motor : \n')
        file.writelines(str(l_movements[0]) + ',' + str(l_movements[-1]) + '\n')
        file.write(l_str)
        file.writelines('\n***********************************************\n')
        file.writelines('Base Motor : \n')
        file.writelines(str(b_movements[0]) + ',' + str(b_movements[-1]) + '\n')
        file.write(b_str)
        file.writelines('\n***********************************************\n')
        file.writelines('Gripper : \n')
        file.writelines(str(a_movements[0]) + ',' + str(a_movements[-1]) + '\n')
        file.write(a_str)
        file.writelines('\n***********************************************\n')
        for d in total_movements:
          json.dump(d,file)
          file.write('\n')
          
    def move(motor,degree,numOfSec):
      command = str(motor) + str(degree) + '|'
      arduino.write(str(command).encode())
      time.sleep(numOfSec)
          
    def pickUp(currentSquare, square):
      # 0 is rightMotor - 1 is left - 2 is base
      print('Going to e2')
      move(1,moves[currentSquare][1],numOfSec = 1)
      move(2,moves[currentSquare][2],numOfSec = 1)
      right_current_pos = moves['o'][0]
      while(right_current_pos <= moves['e2'][0]):
        right_current_pos += 2;
        move(0,right_current_pos,numOfSec= 0.15)
      time.sleep(2)
      arduino.write('3175|'.encode())
      time.sleep(2)  
     
      print('Back to initial pos')
      #TODO : from here should be the picking up part.
      #TODO : also make a move up & down functions for the picking and placing pieces.
      right_current_pos = moves['e2'][0]
      left_current_pos = moves['e2'][1]
      print(right_current_pos)
      print(left_current_pos)
      while(right_current_pos > moves['o'][0] or left_current_pos < 85):
        if(left_current_pos < 90): 
          left_current_pos += 2
          command = '1' + str(left_current_pos) + '|'
          arduino.write(str(command).encode())
          
        if(right_current_pos > moves['o'][0]) : 
          right_current_pos -= 2
          command = '0' + str(right_current_pos) + '|'
          arduino.write(str(command).encode())
        
        time.sleep(0.25)
          
    def makeMove(initial_square,final_square):
      try:
        # move to original pos
        print('Going to initial position') 
        left_current_pos = 40
        while(left_current_pos < 80):
          left_current_pos += 2
          command = '1' + str(left_current_pos) + '|'
          arduino.write(str(command).encode())
          time.sleep(0.25)
          
        command = '2' + str(moves['o'][2]) + '|'
        arduino.write(str(command).encode())
        time.sleep(1)
        command = '0' + str(moves['o'][0]) + '|'
        arduino.write(str(command).encode())
        time.sleep(1)
        command = '1' + str(moves['o'][1]) + '|'
        arduino.write(str(command).encode())
        time.sleep(1)
        arduino.write('3125|'.encode())
        time.sleep(2)
        # move to initial square
        print('Going to e2')
        command = '1' + str(moves[initial_square][1]) + '|'
        arduino.write(str(command).encode())
        time.sleep(1)
        command = '2' + str(moves[initial_square][2]) + '|'
        arduino.write(str(command).encode())
        time.sleep(1)
        right_current_pos = moves['o'][0]
        while(right_current_pos <= moves['e2'][0]):
          right_current_pos += 2;
          command = '0' + str(right_current_pos) + '|'
          arduino.write(str(command).encode())
          time.sleep(0.15)
        time.sleep(2)
        arduino.write('3175|'.encode())
        time.sleep(2)  
        # move to initial square
        print('Back to initial pos')
        # right_interval = abs(moves['o'][0] - moves['e2'][0])
        # left_interval = abs(moves['o'][1] - moves['e2'][1])
        
        right_current_pos = moves['e2'][0]
        left_current_pos = moves['e2'][1]
        print(right_current_pos)
        print(left_current_pos)
        while(right_current_pos > moves['o'][0] or left_current_pos < 85):
          if(left_current_pos < 90): 
            left_current_pos += 2
            command = '1' + str(left_current_pos) + '|'
            arduino.write(str(command).encode())
            
          if(right_current_pos > moves['o'][0]) : 
            right_current_pos -= 2
            command = '0' + str(right_current_pos) + '|'
            arduino.write(str(command).encode())
          
          time.sleep(0.25)
        # # half_r_move = moves['o'][0] // 2
        # # half_l_move = moves['o'][1] // 2
        # # q_r_move = moves['o'][0] // 4
        # # q_l_move = moves['o'][1] // 4
        # # half_r_move = 30
        # # half_l_move = 61
        # # command = '0' + str(q_r_move) + '|'
        # # arduino.write(str(command).encode())
        # # time.sleep(1)
        # # command = 'l' + str(q_l_move) + '|'
        # # arduino.write(str(command).encode())
        # # time.sleep(1)
        # # command = '0' + str(half_r_move) + '|'
        # # arduino.write(str(command).encode())
        # # time.sleep(1)
        # # command = 'l' + str(half_l_move) + '|'
        # # arduino.write(str(command).encode())
        # time.sleep(1)
        # command = '2' + str(moves['o'][2]) + '|'
        # arduino.write(str(command).encode())
        # time.sleep(1)
        # print('done')
        # command = '0' + str(moves['o'][0]) + '|'
        
        # arduino.write(str(command).encode())
        # time.sleep(1)
        # # print(left_current_pos)
        # # while(left_current_pos > moves['o'][1]):
        # #   left_current_pos -= 2
        # #   command = '1' + str(left_current_pos) + '|'
          
        # #   arduino.write(str(command).encode())
        # #   time.sleep(0.25)

        # command = '1' + str(moves['o'][1]) + '|'
        # arduino.write(str(command).encode())
        # time.sleep(2)
        # arduino.write('3125|'.encode())
        # move to e4
        print('Going to e4')
        command = '1' + str(moves[final_square][1]) + '|'
        arduino.write(str(command).encode())
        time.sleep(1)
        command = '2' + str(moves[final_square][2]) + '|'
        arduino.write(str(command).encode())
        time.sleep(1)
        right_current_pos = moves['e2'][0]
        while(right_current_pos <= moves['e4'][0]):
          right_current_pos += 2;
          command = '0' + str(right_current_pos) + '|'
          arduino.write(str(command).encode())
          time.sleep(0.15)
        command = '0' + str(moves[final_square][0]) + '|'
        arduino.write(str(command).encode())
        time.sleep(1)
        arduino.write('3125|'.encode())   
        time.sleep(1)
        print('success ?? ') 
        
      except:
        
        print('something went wrong')

    keyboard_input_thread(sendToArduino,saveToFile,makeMove)
    



main()