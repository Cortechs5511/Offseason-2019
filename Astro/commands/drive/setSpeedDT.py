import math
import wpilib

from wpilib.command import Command
from wpilib.command import TimedCommand

class SetSpeedDT(TimedCommand):

    def __init__(self, timeout = 0):
        super().__init__('SetSpeedDT', timeoutInSeconds = timeout)
        self.requires(self.getRobot().drive)
        self.DT = self.getRobot().drive

        self.Joystick0 = self.getRobot().joystick0
        self.Joystick1 = self.getRobot().joystick1

        self.maxspeed = 1.00 #In addition to normal reducing factor in Drive.py

    def initialize(self):
        self.DT.setDirect()

    def execute(self):
        left = self.Joystick0.getY()
        right = self.Joystick1.getY()
        flip = self.Joystick1.getButton(1) or self.Joystick0.getButton(1)
        if flip == True:
            self.DT.tankDrive(right * self.maxspeed ,left * self.maxspeed)
        self.DT.tankDrive(-left * self.maxspeed ,-right * self.maxspeed)

    def interrupted(self):
        self.end()

    def end(self):
        self.DT.tankDrive(0,0)
