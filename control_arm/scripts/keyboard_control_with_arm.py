import threading
import serial 
import keyboard
import json
import time

import sys
sys.path.insert(0,"..")

from arm_model.arm import Arm

 

# TODO : format this file and restructure !! 

def keyboard_input_thread(callback,arm,save_to_file):
  
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
            arm_pos += 10
            callback(arm_pos,3)
            if is_recording : a_movements.append(arm_pos)
            
        elif c == 'v':
            arm_pos -= 10
            callback(arm_pos,3)
            if is_recording : a_movements.append(arm_pos)
        
        elif c == 'r':
            if(not is_recording):
                is_recording = True
                print('Recording Started ...')
                print('press u to save')

        elif c == 'k':
            left_pos += 1
            right_pos -= 1
            callback(left_pos,1)
            callback(right_pos,0)
            if is_recording: 
                l_movements.append(left_pos)
                r_movements.append(right_pos)

        elif c == 'j':
            left_pos -= 1
            right_pos += 1
            callback(left_pos,1)
            callback(right_pos,0)
            if is_recording: 
                l_movements.append(left_pos)
                r_movements.append(right_pos)

        elif c == 'l':
            left_pos += 1
            right_pos += 1
            callback(left_pos,1)
            callback(right_pos,0)
            if is_recording: 
                l_movements.append(left_pos)
                r_movements.append(right_pos)

        elif c == 'h':
            left_pos -= 1
            right_pos -= 1
            callback(left_pos,1)
            callback(right_pos,0)
            if is_recording: 
                l_movements.append(left_pos)
                r_movements.append(right_pos)

        elif c == 'u':
            is_recording = False
            save_to_file(r_movements,l_movements,b_movements,a_movements,movements)
            print('Saving ...')

        elif c == 'm':
            print('Trying to play e2 to e4............')
            arm.make_move('e4','e2')
        
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
    arm = Arm(arduino_conn= arduino,gripper_is_open=True)

    def sendToArduino(pos,motor):       
        try:
            command = str(motor) + str(pos) + '|'
            print('Motor : ' + str(motor) + ' Angle : ' + str(pos))
            arduino.write(str(command).encode())
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
                  
   
    


    keyboard_input_thread(sendToArduino,arm,saveToFile)
    



main()