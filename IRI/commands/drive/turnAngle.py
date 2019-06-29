import math
import wpilib

from wpilib import SmartDashboard
from wpilib.command import Command
from wpilib.command import TimedCommand

class TurnAngle(TimedCommand):

    def __init__(self, angle = 0, timeout = 0):
        super().__init__('TurnAngle', timeoutInSeconds = timeout)
        self.requires(self.getRobot().drive)
        self.DT = self.getRobot().drive
        self.angle = angle

    def initialize(self):
        p = SmartDashboard.getNumber("DriveAngle_P", 0.02)
        i = SmartDashboard.getNumber("DriveAngle_I", 0)
        d = SmartDashboard.getNumber("DriveAngle_D", 0.01)
        self.DT.setGainsAngle(p, 0, d, 0)
        self.DT.setAngle(self.angle)

    def execute(self):
        self.DT.tankDrive()

    def isFinished(self):
        return (abs(self.angle-self.DT.getAngle())<2 and self.DT.getAvgAbsVelocity()<0.05) or self.isTimedOut()

    def interrupted(self):
        self.end()

    def end(self):
        self.DT.setMode("Direct")
        self.DT.tankDrive(0,0)
