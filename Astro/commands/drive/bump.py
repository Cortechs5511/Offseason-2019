import math
import wpilib

from wpilib.command import Command
from wpilib.command import TimedCommand
from wpilib import SmartDashboard

class Bump(Command):

    def __init__(self):
        self.debug = True
        super().__init__('Bump', timeoutInSeconds = timeout)
        self.requires(self.getRobot().drive)
        self.DT = self.getRobot().drive

        self.accel = wpilib.BuiltInAccelerometer()

    def execute(self):
        self.accelX = self.accel.getX()
        self.accelY = self.accel.getY()

        if self.debug:
            SmartDashboard.putNumber("X", self.accelX)
            SmartDashboard.putNumber("Y", self.accelY)
    def isFinished(self):
        return False
