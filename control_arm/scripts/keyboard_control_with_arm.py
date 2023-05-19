import threading
import serial 
import keyboard
import json
import time

import sys
sys.path.insert(0,"..")

from arm_model.arm import Arm

 

# TODO : format this file and restructure !! 

def keyboard_input_thread(callback,arm,save_to_file,save_to_json):
    
  

  def keyboard_input():
    r_movements = []
    l_movements = []
    b_movements = []
    a_movements = []
    movements = []
    is_recording = False
    right_pos = 24
    left_pos = 106
    base_pos = 90
    arm_pos = 110

    

    number_of_records = 0
    
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
                number_of_records += 1
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
            # save_to_file(r_movements,l_movements,b_movements,a_movements,movements,number_of_records)
            action = str(input())
            if(action == 'u'):
                save_to_json(base_pos,right_pos,left_pos,None,None,None,None)
            elif(action == 'p'):
                save_to_json(None,None,None,right_pos,left_pos,None,None)
            else:
                save_to_json(None,None,None,None,None,right_pos,left_pos)
            print('Saving ...')

        elif c == 'm':
            # possible Demo scenario 
            # arm.make_move('d2','d4','p',False)
            # arm.make_move('g2','g3','p',False)
            # arm.make_move('g5','o','p',False)
            # arm.make_move('c1','g5','p',False)
            # arm.make_move('e2','e3','p',False)
            # arm.make_move('d1','h5','k',False)
            # print('Trying to play e2 to e4............')
            arm.make_move('e2','e4','p',False)
            arm.make_move('g1','f3','p',False)
            arm.make_move('f1','c4','p',False)
            arm.make_move('d2','d3','p',False)
            # arm.make_move('c1','c2','k',False)
            # arm.make_move('c2','c3','k',False)
            # arm.make_move('b1','c1','k',False)
            # arm.make_move('a1','c2','k',False)
            #castle
            arm.make_special_move('e1','g1','k','h1','f1','p','castle')
            # arm.make_move('e1','g1','k',False)
            # arm.make_move('h1','f1','p',True)
        
        else:
            # print(c + ' is Pressed')
            print('Nothing Happened')
        
        if(is_recording):  
            movements.append({'r': right_pos,'l':left_pos,'b':base_pos,'a':arm_pos})
      
  thread = threading.Thread(target=keyboard_input)
  thread.start()


def main():
    arduino = serial.Serial('COM3', 9600, timeout=0.1)
    # moves = {'o':[16,48,145],'e2': [65,74,111],'e4':[61,72,97]}
    arm = Arm(arduino_conn= arduino,gripper_is_open=True)
    # arm.arm_initialize(True)
    def sendToArduino(pos,motor):       
        try:
            command = str(motor) + str(pos) + '|'
            print('Motor : ' + str(motor) + ' Angle : ' + str(pos))
            arduino.write(str(command).encode())
            # print(arduino.readall())
        except:
            arduino.close()

    def save_to_json(base,ur,ul,dpr,dpl,dkr,dkl):
        move = str(input())
        json = {
            move: {
                "B":0,
                "UL": 0,
                "UR": 0,
                "DPL": 0,
                "DPR": 0,
                "DKL": 0,
                "DKR": 0,
            }
        }
        if(base != None and ur != None and ul != None):
            json[move]["B"] = base 
            json[move]["UR"] = ur
            json[move]['UL'] = ul
        if(dpr != None):
            json[move]["DPR"] = dpr 
            json[move]["DPL"] = dpl
        if(dkr != None):
            json[move]["DKR"] = dkr
            json[move]["DKL"] = dkl
            
        print(str(json))

    def saveToFile(r_movements,l_movements,b_movements,a_movements,total_movements,number_of_records):
      r_str = ','.join(map(str, r_movements))
      l_str = ','.join(map(str, l_movements))
      b_str = ','.join(map(str, b_movements))
      a_str = ','.join(map(str, a_movements))
      # Open the file in write mode
      path = f"../outputs/new_record{number_of_records}.txt"
      with open(path, "w") as file:
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
                  
   
    


    keyboard_input_thread(sendToArduino,arm,saveToFile,save_to_json)
    



main()
