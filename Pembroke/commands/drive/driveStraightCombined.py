import math
import wpilib
from wpilib import SmartDashboard
from wpilib.command import Command
from wpilib.command import TimedCommand

class DriveStraightCombined(TimedCommand):

    def __init__(self, distance = 10, angle = 0, timeout = 0):
        super().__init__('DriveStraightCombined', timeoutInSeconds = timeout)

        self.requires(self.getRobot().drive)
        self.DT = self.getRobot().drive

        self.distance = distance/12
        self.angle = angle

    def initialize(self):
        p = SmartDashboard.getNumber("DriveStraight_P", 0.01)
        i = SmartDashboard.getNumber("DriveStraight_I", 0)
        d = SmartDashboard.getNumber("DriveStraight_D", 0)
        self.DT.setGains(p, i, d, 0)
        self.distance = self.distance + self.DT.getAvgDistance()
        self.DT.setCombined(distance=self.distance, angle=self.angle)

    def execute(self):
        self.DT.tankDrive()

    def isFinished(self):
        return (abs(self.distance-self.DT.getAvgDistance())<0.1 and self.DT.getAvgAbsVelocity()<0.1) or self.isTimedOut()

    def interrupted(self):
        self.end()

    def end(self):
        self.DT.setMode("Direct")
        self.DT.tankDrive(0,0)
