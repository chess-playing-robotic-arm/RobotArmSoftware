import time

RIGHT = 0
LEFT = 1
BASE = 2
GRIPPER = 3
STEP = 2

moves = {'o':[16,48,145],'e2': [65,74,111],'e4':[61,72,97]}


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
        if(self.pos < new_pos): # ex: 90 -> 180
            for i in range(self.pos, new_pos ,STEP):
                command = f'{self.id}{i}|'.encode()
                commands.append(command)
        elif(self.pos > new_pos):
            for i in range(self.pos,new_pos,-STEP):
                command = f'{self.id}{i}|'.encode()
                commands.append(command)
        else:
            return
        return commands
    


    def __str__(self):
        return f'{self.id}: {self.name}'

    

    

    


class Arm():
    def __init__(self,arduino_conn,gripper_is_open):
        self.arduino_conn = arduino_conn
        self.base = Motor(None,'base',2)
        self.right = Motor(None,'right',0)
        self.left = Motor(None,'left',1)
        self.gripper_is_open = gripper_is_open

    def open_gripper(self):
        self.execute(GRIPPER,125)
        self.gripper_is_open = True

    def grab(self):
        self.execute(GRIPPER,175)
        self.gripper_is_open = False



    #TODO: there has to be a better way to refactor this junk
    def execute(self,motor,degree):
        print(f'Motor is  : {motor}, degree to go to : {degree}')
        
        if (self.left is None or self.right is None):
            command = f'{motor}{degree}|'.encode()
            self.arduino_conn.write(command)
            time.sleep(0.10) 
        else:
            if(motor == RIGHT):
                if(degree < self.right): # trying to retract the right arm ex: 180 -> 40
                    
                    for i in range(self.right, degree ,-STEP):
                        command = f'{motor}{i}|'.encode()
                        self.arduino_conn.write(command)
                        time.sleep(0.10) 
                else: # ex: 40 -> 180
                    for i in range(self.right, degree ,STEP):
                        command = f'{motor}{i}|'.encode()
                        self.arduino_conn.write(command)
                        time.sleep(0.10) 
            elif(motor == LEFT):
                if(degree < self.left): # trying to retract the right arm ex: 180 -> 40
                    for i in range(self.left, degree ,-STEP):
                        command = f'{motor}{i}|'.encode()
                        self.arduino_conn.write(command)
                        time.sleep(0.10) 
                else: # ex: 40 -> 180
                    for i in range(self.left, degree ,STEP):
                        command = f'{motor}{i}|'.encode()
                        self.arduino_conn.write(command)
                        time.sleep(0.10)
            else:
                command = f'{motor}{degree}|'.encode()
                self.arduino_conn.write(command)
                time.sleep(0.10) 


    def arm_initialize(self,gripper_to_be_open):
        self.execute(RIGHT,26)  # move right motor to 40 degrees.
        self.right = 26
        self.execute(LEFT,80)  # move left motor to 60 degrees.
        self.left = 80
        self.execute(BASE,150)  # move base motor to 90 degrees.
        self.base = 150
        if(gripper_to_be_open):
            self.open_gripper()

    def horizontal_pickup(self):
        while(self.right > 25 or self.left < 85):
          if(self.left < 90): 
            self.left += 2
            command = '1' + str(self.left) + '|'
            self.arduino_conn.write(str(command).encode())
            
          if(self.right > 25) : 
            self.right -= 2
            command = '0' + str(self.right) + '|'
            self.arduino_conn.write(str(command).encode())
          
          time.sleep(0.25)
    
    def make_move(self,initial_sq,target_sq):
        try:
            # move to original pos
            print('Going to initial position') 
            self.arm_initialize(gripper_to_be_open= True)
            time.sleep(2)

            # move to initial square
            print(f'Going to {initial_sq}')
            self.execute(LEFT,moves[initial_sq][1])
            self.left = moves[initial_sq][1]
            time.sleep(1)
            self.execute(BASE,moves[initial_sq][2])
            self.base = moves[initial_sq][2]
            time.sleep(1)
            self.execute(RIGHT,moves[initial_sq][0])
            self.right = moves[initial_sq][0]
            time.sleep(2)
            self.grab()
            time.sleep(2)

            #! horizontal pick up
            self.horizontal_pickup()

            # move to initial pos
            print('Back to initial pos')
            self.execute(BASE,150)
            # self.arm_initialize(gripper_to_be_open= False)
            time.sleep(2)
            
            # move to Target square
            print(f'Going to {target_sq}')
            self.execute(LEFT,moves[target_sq][1])
            self.left = moves[target_sq][1]
            time.sleep(1)
            self.execute(BASE,moves[target_sq][2])
            self.base = moves[target_sq][2]
            time.sleep(1)
            self.execute(RIGHT,moves[target_sq][0])
            self.right = moves[target_sq][0]
            time.sleep(1)
            self.open_gripper()
            time.sleep(1)

            # back to initial pos
            print('Back to initial pos')
            self.arm_initialize(gripper_to_be_open= False)
            time.sleep(2)
            print('success ?? ') 
        
        except Exception as e:
            print('something went wrong !')
            print(f'Here is there Error : {e}')
