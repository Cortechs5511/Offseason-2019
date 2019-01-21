import math
import ctre
import wpilib
from wpilib import SmartDashboard
from wpilib.command.subsystem import Subsystem
from wpilib import SmartDashboard as sd

from sim import simComms

class HatchMech(subsystem):

    def __init__(self, Robot):
        self.piston = wpilib.DoubleSolenoid(0,1)

    def set(self, trigger):
        if state == 2 and trigger == "Out":
            state = wpilib.DoubleSolenoid.Value.kForward
        elif state == 1 and trigger == "In":
            state = wpilib.DoubleSolenoid.Value.kReverse
        else:
            pass

    def setMode(self, mode):
        if mode == "Forward":
            state = wpilib.DoubleSolenoid.Value.kForward
        elif mode == "Reverse":
            state = wpilib.DoubleSolenoid.Value.kReverse
        else:
            pass

        self.piston.set(state)
        sd.putNumber("Piston",state)
