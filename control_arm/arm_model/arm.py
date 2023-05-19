import time

RIGHT = 0
LEFT = 1
BASE= 2
GRIPPER = 3
STEP = 2

# moves = {'o':[16,48,145],'e2': [64,72,114],'e4':[61,72,97]}
moves = {
    "e1":
    {
        "B": 68,
        "UL": 140,
        "UR": 46,
        "DPL": 118,
        "DPR": 60,
        "DKL": 128,
        "DKR": 58
    },
    "e2":
    {
        "B": 76,
        "UL": 139,
        "UR": 39,
        "DPL": 118,
        "DPR": 60,
        "DKL": 124,
        "DKR": 54
    },
    "e3": 
    {
        "B": 84,
        "UL": 138,
        "UR": 36,
        "DPL": 116, 
        "DPR": 58, 
        "DKL": 122, 
        "DKR": 52
    },
    "e4": 
    {
        "B": 90,
        "UL": 138,
        "UR": 36,
        "DPL": 116, 
        "DPR": 58, 
        "DKL": 122, 
        "DKR": 52
    },
    "g1":
    {
        "B": 72,
        "UL": 162,
        "UR": 66,
        "DPL": 144,
        "DPR": 84,
        "DKL": 149,
        "DKR": 79 
    },
    "g2":
    {
        "B": 80,
        "UL": 158,
        "UR": 64,
        "DPL": 142,
        "DPR": 80,
        "DKL": 144,
        "DKR": 78 
    },
    "g3":
    {
        "B": 86,
        "UL": 154,
        "UR": 60,
        "DPL": 138,
        "DPR": 76,
        "DKL": 142,
        "DKR": 72 
    },
    "f3":
    {
        "B": 84,
        "UL": 148,
        "UR": 44,
        "DPL": 126,
        "DPR": 66,
        "DKL": 122, # to be changed
        "DKR": 52 # to be changed
    },
    "f1":
    {
        "B": 70,
        "UL": 148,
        "UR": 54,
        "DPL": 132,
        "DPR": 70,
        "DKL": 122, # to be changed
        "DKR": 52 # to be changed
    },
    "c1":
    {
        "B": 64,
        "UL": 132,
        "UR": 22,
        "DPL": 104,
        "DPR": 50,
        "DKL": 110, 
        "DKR": 44 
    },
    "c2":
    {
        "B": 71,
        "UL": 132,
        "UR": 14,
        "DPL": 100,
        "DPR": 46,
        "DKL": 110, 
        "DKR": 40 
    },
    "c3":
    {
        "B": 81,
        "UL": 130,
        "UR": 12,
        "DPL": 98,
        "DPR": 44,
        "DKL": 106, 
        "DKR": 40 
    },
    "c4":
    {
        "B": 90,
        "UL": 140,
        "UR": 2,
        "DPL": 100,
        "DPR": 42,
        "DKL": 122, # to be changed
        "DKR": 52 # to be changed
    },
    "d2":
    {
        "B": 74,
        "UL": 132,
        "UR": 30,
        "DPL": 110,
        "DPR": 52,
        "DKL": 122, # to be changed
        "DKR": 52 # to be changed
    },
    "d3":
    {
        "B": 82,
        "UL": 130,
        "UR": 28,
        "DPL": 108,
        "DPR": 50,
        "DKL": 122, # to be changed
        "DKR": 52 # to be changed
    },
    "h1":
    {
        "B": 76,
        "UL": 170,
        "UR": 92,
        "DPL": 160,
        "DPR": 102,
        "DKL": 124,# to be changed
        "DKR": 54 # to be changed
    },
    
    "f2":
    {
        "B": 76,
        "UL": 148,
        "UR": 50,
        "DPL": 130,
        "DPR": 68,
        "DKL": 134,
        "DKR": 64
    },
    "f4":
    {
        "B": 92,
        "UL": 144,
        "UR": 46,
        "DPL": 126,
        "DPR": 64,
        "DKL": 130,
        "DKR": 60 
    },
    "d1":
    {
        "B": 67,
        "UL": 136,
        "UR": 34,
        "DPL": 114,
        "DPR": 56,
        "DKL": 120,
        "DKR": 50 
    },
    "d4":
    {
        "B": 90,
        "UL": 134,
        "UR": 24,
        "DPL": 108,
        "DPR": 50,
        "DKL": 112,
        "DKR": 46
    },
    "b1":
    {
        "B": 58,
        "UL": 128,
        "UR": 12,
        "DPL": 96,
        "DPR": 46,
        "DKL": 104, 
        "DKR": 38 
    },
    "a1":
    {
        "B": 52,
        "UL": 138,
        "UR": 0,
        "DPL": 88,
        "DPR": 42,
        "DKL": 98, 
        "DKR": 32 
    },
    "h5":
    {
        "B": 98,
        "UL": 170,
        "UR": 76,
        "DPL": 154,
        "DPR": 92,
        "DKL": 154, 
        "DKR": 92 
    },
    "g5":
    {
        "B": 99,
        "UL": 154,
        "UR": 60,
        "DPL": 138,
        "DPR": 76,
        "DKL": 140, 
        "DKR": 74 
    },
    "o":
    {
        "B": 40,
        "UL": 132,
        "UR": 26,
        "DPL": 108,
        "DPR": 50,
        "DKL": 112, 
        "DKR": 42 
    },
}

def merge_alternatively(lst1, lst2):
        if not lst1:
            return lst2
        if not lst2:
            return lst1
        return [lst1[0], lst2[0]] + merge_alternatively(lst1[1:], lst2[1:])


class Motor():
    def __init__(self,pos,name,motor_id):
        self.pos = pos
        self.name = name
        self.id = motor_id

    def update(self,new_pos):
        self.pos = new_pos

    # returns: the list of commands that should be executed by the arm.
    def rotate(self,new_pos):
        commands = []
        # print(self.pos)
        # print(new_pos)
        if(self.pos < new_pos): # ex: 90 -> 180
            for i in range(self.pos, new_pos+1 ,STEP):
                command = f'{self.id}{i}|'.encode()
                commands.append(command)
        elif(self.pos > new_pos): # ex: 180 -> 90
            for i in range(self.pos,new_pos-1,-STEP):
                command = f'{self.id}{i}|'.encode()
                commands.append(command)
        else:
            return
        commands.append(new_pos)
        return commands
    

    def __str__(self):
        return self.name


class Arm():
    def __init__(self,arduino_conn,gripper_is_open):
        self.arduino_conn = arduino_conn
        self.base = Motor(None,'base',2)
        self.right = Motor(None,'right',0)
        self.left = Motor(None,'left',1)
        self.gripper_is_open = gripper_is_open

    def open_gripper(self,deg=130):
        # command = f'3{deg}|'.encode()
        if(deg==130):
            for i in range(5):
                self.arduino_conn.write('3130|'.encode())
        else:
            for i in range(5):
                self.arduino_conn.write('3110|'.encode())
        self.gripper_is_open = True

    def grab(self):
        for i in range(8):
            self.arduino_conn.write('3175|'.encode())
        self.gripper_is_open = False

    def execute(self,motor,degree):
        print(f'Motor is: {motor}, degree to go to : {degree}')
        if(motor.pos == None):
            # print(f'{motor.pos}')
            command = f'{motor.id}{degree}|'.encode()
            # print(command)
            self.arduino_conn.write(command)   
        else:
            commands = motor.rotate(degree)
            if(commands == None):
                return
            # print(f'the motor is not null')
            # print(commands)
            for command in commands:
                self.arduino_conn.write(command)
                time.sleep(0.05)
        motor.update(degree)

    def parallel_execute(self,first_motor,second_motor,first_deg,second_deg):
        print(f'Both {first_motor} and {second_motor} are going to {first_deg} and {second_deg} at the same time')
        f_commands = first_motor.rotate(first_deg) # ex: 5 commands
        s_commands = second_motor.rotate(second_deg) # ex: 6 commands
        commands = merge_alternatively(f_commands,s_commands)
        if(commands == None or commands == []): return
        for command in commands:
            self.arduino_conn.write(command)
            time.sleep(0.05)
        first_motor.update(first_deg)
        second_motor.update(second_deg)

    def arm_initialize(self,gripper_to_be_open):
        # self.execute(self.right,35)  # move right motor to 40 degrees.
        # self.execute(self.left,106)  # move left motor to 60 degrees.
        self.execute(self.right,24)  # move right motor to 40 degrees.
        self.execute(self.left,130)  # move left motor to 60 degrees.
        
        # self.parallel_execute(self.right,self.left,24,130)
        self.execute(self.base,20)  # move base motor to 90 degrees.
        if(gripper_to_be_open):
            self.open_gripper()

    def go_to_origin(self,right_deg,left_deg):
        self.parallel_execute(self.right,self.left,right_deg,left_deg)
        self.execute(self.base,20)

   
    def make_move(self,initial_sq,target_sq,piece_type,special_bool):
        try:
            # move to original pos
            print('Going to initial position') 
            self.arm_initialize(gripper_to_be_open= True)
            time.sleep(2)

            self.parallel_execute(self.right,self.left,24,130)
            time.sleep(1)

            # move to initial square
            init_move = moves[initial_sq]
            final_sq = moves[target_sq]

            print(f'Going to {moves[initial_sq]}')

            self.parallel_execute(self.right,self.left,init_move["UR"],init_move["UL"])
            time.sleep(0.1)
            
            self.execute(self.base,init_move["B"])   
            time.sleep(0.5)
            if(piece_type == 'p'):
                self.parallel_execute(self.left,self.right,init_move["DPL"],init_move["DPR"])
            else:
                self.parallel_execute(self.left,self.right,init_move["DKL"],init_move["DKR"])
            time.sleep(0.5)
            
            
            self.grab()
            if(special_bool == True):
                print('Iam probably castling')
                self.execute(self.base,40)
            time.sleep(2)

            #! horizontal pick up
            
            print('preforming pick up motion')
            self.parallel_execute(self.right,self.left,init_move["UR"],init_move["UL"])
            time.sleep(0.5)

            # move to Target square
            print(f'Going to {target_sq}')
            if(special_bool):
                self.parallel_execute(self.left,self.right,final_sq["UL"],final_sq["UR"])
                time.sleep(1)
                if(piece_type == 'p'):
                    self.parallel_execute(self.left,self.right,final_sq["DPL"],final_sq["DPR"])
                else:
                    self.parallel_execute(self.left,self.right,final_sq["DKL"],final_sq["DKR"])
                time.sleep(1)
                self.execute(self.base,final_sq["B"])
            else:
                self.execute(self.base,final_sq["B"])
                time.sleep(1)
                self.parallel_execute(self.left,self.right,final_sq["UL"],final_sq["UR"])
                time.sleep(1)
                if(piece_type == 'p'):
                    self.parallel_execute(self.left,self.right,final_sq["DPL"],final_sq["DPR"])
                else:
                    self.parallel_execute(self.left,self.right,final_sq["DKL"],final_sq["DKR"])
             
            time.sleep(1)
            self.open_gripper()
            time.sleep(1)

            # back to initial pos
            print('Back to initial pos')
            # self.arm_initialize(gripper_to_be_open= False)
            self.go_to_origin(final_sq["UR"],final_sq["UL"])
            time.sleep(0.5)
            # self.execute(self.right,35)  # move right motor to 40 degrees.
            # time.sleep(0.5)
            # self.execute(self.left,106)  # move left motor to 60 degrees.
            # time.sleep(0.5)
            print('success ?? ') 
        
        except Exception as e:
            print('something went wrong !')
            print(f'Here is the Error : {e}')


    def make_special_move(self,initial_sq,target_sq,piece_type,s_initial_sq,s_target_sq,s_piece_type,move_type):
        if(move_type == 'castle'):
            try:
                # move to original pos
                print('Going to initial position') 
                self.arm_initialize(gripper_to_be_open= True)
                time.sleep(1)

                self.parallel_execute(self.right,self.left,24,130)
                time.sleep(1)

                # move to initial square
                init_move = moves[initial_sq]
                final_sq = moves[target_sq]

                ##! First execution in this case King
                print(f'Going to {initial_sq}')

                self.parallel_execute(self.right,self.left,init_move["UR"],init_move["UL"])
                time.sleep(0.1)
                
                self.execute(self.base,init_move["B"])   
                time.sleep(0.5)
                if(piece_type == 'p'):
                    self.parallel_execute(self.left,self.right,init_move["DPL"],init_move["DPR"])
                else:
                    self.parallel_execute(self.left,self.right,init_move["DKL"],init_move["DKR"])
                time.sleep(0.5)
                
                
                self.grab()
                time.sleep(0.5)
                # self.execute(self.base,50)
                
                #! horizontal pick up
                
                print('preforming pick up motion')
                self.parallel_execute(self.right,self.left,init_move["UR"],init_move["UL"])
                time.sleep(0.5)

                # move to Target square
                print(f'*****************Going to {target_sq}')
                self.execute(self.base,final_sq["B"])
                time.sleep(1)

                self.parallel_execute(self.left,self.right,final_sq["UL"],final_sq["UR"])
                time.sleep(1)

                if(piece_type == 'p'):
                    self.parallel_execute(self.left,self.right,final_sq["DPL"],final_sq["DPR"])
                else:
                    self.parallel_execute(self.left,self.right,final_sq["DKL"],final_sq["DKR"])
               
                
                
                time.sleep(1)
                self.open_gripper(125)
                time.sleep(1)

                self.parallel_execute(self.left,self.right,final_sq["UL"],final_sq["UR"])
                time.sleep(1)

                ####################################################################
                
                # self.parallel_execute(self.right,self.left,final_sq["UL"],final_sq["UR"])
                time.sleep(1)

                    # move to initial square
                init_move = moves[s_initial_sq]
                final_sq = moves[s_target_sq]
                
                print(f'*****************Going to {s_initial_sq}')
                self.parallel_execute(self.right,self.left,init_move["UR"],init_move["UL"])
                time.sleep(0.5)
                
                self.execute(self.base,init_move["B"])   
                time.sleep(0.5)
                if(s_piece_type == 'p'):
                    self.parallel_execute(self.left,self.right,init_move["DPL"],init_move["DPR"])
                else:
                    self.parallel_execute(self.left,self.right,init_move["DKL"],init_move["DKR"])
                time.sleep(0.5)
                
                
                self.grab()
                time.sleep(0.5)
                self.execute(self.base,50)

                print('preforming pick up motion')
                self.parallel_execute(self.right,self.left,init_move["UR"],init_move["UL"])
                time.sleep(0.5)

                # move to Target square
                print(f'**********************Going to {s_target_sq}')
                
                self.parallel_execute(self.left,self.right,final_sq["UL"],final_sq["UR"])
                time.sleep(1)
                self.execute(self.base,final_sq["B"])
                time.sleep(1)

                if(s_piece_type == 'p'):
                    self.parallel_execute(self.left,self.right,final_sq["DPL"],final_sq["DPR"])
                else:
                    self.parallel_execute(self.left,self.right,final_sq["DKL"],final_sq["DKR"])
                time.sleep(1)

                
                
                
                self.open_gripper()
                time.sleep(1)
                self.parallel_execute(self.left,self.right,final_sq["UL"],final_sq["UR"])
                time.sleep(1)

                # back to initial pos
                print('Back to initial pos')
                # self.arm_initialize(gripper_to_be_open= False)
                self.execute(self.base,50)
                self.go_to_origin(final_sq["UR"],final_sq["UL"])
                time.sleep(0.5)
                self.execute(self.right,35)  # move right motor to 40 degrees.
                time.sleep(0.5)
                self.execute(self.left,106)  # move left motor to 60 degrees.
                time.sleep(1)
                print('success ?? ') 
            
            except Exception as e:
                print('something went wrong !')
                print(f'Here is there Error : {e} , {e.args}')



    def __str__(self):
        return f'base @ {self.base.pos}, right @ {self.right.pos}, left @ {self.left.pos}'
