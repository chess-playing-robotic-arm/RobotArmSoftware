
import sys
sys.path.insert(0,"..")

from arm_model.arm import Arm

class FakeArduino():
    def write(self,command):
        print(command.decode())

fake_arduino = FakeArduino()
arm = Arm(fake_arduino,True)

print(arm)

arm.make_move('e2','e4')