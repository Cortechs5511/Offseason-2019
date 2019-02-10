import math
import wpilib

from wpilib import SmartDashboard
from wpilib.command import Command
from wpilib.command import TimedCommand

class RelativeTurn(TimedCommand):

    def __init__(self, angle = 90, timeout = 0):
        super().__init__('RelativeTurn', timeoutInSeconds = timeout)
        self.requires(self.getRobot().drive)
        self.DT = self.getRobot().drive
        self.angle = angle

    def initialize(self):
        StartAngle = self.DT.getAngle()
        self.EndAngle = StartAngle + self.angle
        self.DT.setMode('Direct')

    def execute(self):
        self.DT.tankDrive(-0.25 , 0.25)

    def isFinished(self):
        CurrentAngle = self.DT.getAngle()
        if CurrentAngle >= self.EndAngle:
            return True
        else: return False

    def interrupted(self):
        self.end()

    def end(self):
        self.DT.tankDrive(0,0)
