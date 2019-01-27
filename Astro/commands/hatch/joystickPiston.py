import math
import wpilib

from wpilib.command import Command
from wpilib.command import TimedCommand

class JoystickPiston(TimedCommand):
    def __init__(self, timeout = 0):
        super().__init__('JoystickPiston')
        self.requires(self.getRobot().pistons)
        self.pistons = self.getRobot().pistons

        self.Joystick0 = self.getRobot().joystick0

    def exectute(self):
        trig1 = self.Joystick0.getButton(3)
        trig2 = self.Joystick0.getButton(4)
        if trig1 == True and trig2 == False:
            trigger = "In"
        elif trig1 == False and trig2 == True:
            trigger = "Out"
        else:
            trigger = "None"
        self.pistons.set(trigger)

    def interrupted(self):
        self.end()

    def end(self):
        self.pistons.setMode("Reverse")
