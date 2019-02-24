import math
import wpilib

from wpilib.command import Command
from wpilib.command import TimedCommand

class DriveStraightTime(TimedCommand):

    def __init__(self, speed = 0, timeout = 3):
        super().__init__('DriveStraightTime', timeoutInSeconds = timeout)
        self.requires(self.getRobot().drive)
        self.DT = self.getRobot().drive
        self.speed = speed
        self.endTime = timeout

    def initialize(self):
        StartAngle = self.DT.getAngle()
        self.DT.setMode("DriveStraight", name=None, distance=0, angle=StartAngle)

    def execute(self):
        self.DT.tankDrive(self.speed, self.speed)

    def isFinished(self):
        if self.timeSinceInitialized() > self.endTime:
            return True
        else: return False

    def interrupted(self):
        self.end()

    def end(self):
        self.DT.left.set(0)
        self.DT.right.set(0)
