import time

RIGHT = 0
LEFT = 1
BASE= 2
GRIPPER = 3
STEP = 2

moves = {'o':[16,48,145],'e2': [64,72,114],'e4':[61,72,97]}


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
        print(self.pos)
        print(new_pos)
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

    def open_gripper(self):
        self.arduino_conn.write('3125|'.encode())
        self.gripper_is_open = True

    def grab(self):
        self.arduino_conn.write('3175|'.encode())
        self.gripper_is_open = False

    def execute(self,motor,degree):
        print(f'Motor is: {motor}, degree to go to : {degree}')
        if(motor.pos == None):
            print(f'{motor.pos}')
            command = f'{motor.id}{degree}|'.encode()
            print(command)
            self.arduino_conn.write(command)   
        else:
            commands = motor.rotate(degree)
            if(commands == None):
                return
            print(f'the motor is not null')
            print(commands)
            for command in commands:
                self.arduino_conn.write(command)
                time.sleep(0.1)
        motor.update(degree)

    def parallel_execute(self,first_motor,second_motor,first_deg,second_deg):
        print(f'Both {first_motor} and {second_motor} are going to {first_deg} and {second_deg} at the same time')
        f_commands = first_motor.rotate(first_deg) # ex: 5 commands
        s_commands = second_motor.rotate(second_deg) # ex: 6 commands
        commands = merge_alternatively(f_commands,s_commands)
        for command in commands:
            self.arduino_conn.write(command)
            time.sleep(0.1)
        first_motor.update(first_deg)
        second_motor.update(second_deg)

    def arm_initialize(self,gripper_to_be_open):
        self.execute(self.right,26)  # move right motor to 40 degrees.
        self.execute(self.left,80)  # move left motor to 60 degrees.
        self.execute(self.base,150)  # move base motor to 90 degrees.
        if(gripper_to_be_open):
            self.open_gripper()

    #TODO : to be deleted 
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
            self.parallel_execute(self.right,self.left,25,95)
            time.sleep(0.5)
            
            self.execute(self.base,moves[initial_sq][2])   
            time.sleep(1)

            self.parallel_execute(self.left,self.right,moves[initial_sq][1],moves[initial_sq][0])
            time.sleep(1)
            
            
            self.grab()
            time.sleep(2)

            #! horizontal pick up
            # self.horizontal_pickup()
            print('preforming pick up motion')
            self.parallel_execute(self.left,self.right,95,25)

            # move to initial pos
            # print('Back to initial pos')
            # self.execute(BASE,150)
            # self.arm_initialize(gripper_to_be_open= False)
            time.sleep(1)
            
            # move to Target square
            print(f'Going to {target_sq}')
            self.execute(self.base,moves[target_sq][2])
            time.sleep(1)
            self.parallel_execute(self.left,self.right,moves[target_sq][1],moves[target_sq][0])
            # self.execute(LEFT,moves[target_sq][1])
            # self.left = moves[target_sq][1]
            # time.sleep(1)
            # self.execute(RIGHT,moves[target_sq][0])
            # self.right = moves[target_sq][0]
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

    def __str__(self):
        # if (self.base.pos == None and self.right.pos == None and self.left.pos == None):
        #     return 'motors not initialized yet !'
        # else:
        return f'base @ {self.base.pos}, right @ {self.right.pos}, left @ {self.left.pos}'