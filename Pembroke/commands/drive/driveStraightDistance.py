import math
import wpilib
from wpilib import SmartDashboard

from wpilib.command import Command
from wpilib.command import TimedCommand

class DriveStraightDistance(TimedCommand):

    def __init__(self, distance = 10, timeout = 0):
        super().__init__('DriveStraightDistance', timeoutInSeconds = timeout)
        self.requires(self.getRobot().drive)
        self.DT = self.getRobot().drive
        self.setpoint = distance/12

    def initialize(self):
        p = SmartDashboard.getNumber("DriveStraight_P", 0.01)
        i = SmartDashboard.getNumber("DriveStraight_I", 0)
        d = SmartDashboard.getNumber("DriveStraight_D", 0)
        self.DT.setGains(p, i, d, 0)
        StartAngle = self.DT.getAngle()
        self.DT.setMode("Combined", name=None, distance=self.setpoint, angle=StartAngle)

    def execute(self):
        self.DT.tankDrive()

    def isFinished(self):
        return (abs(self.setpoint-self.DT.getAvgDistance())<0.03 and self.DT.getAvgAbsVelocity()<0.05) or self.isTimedOut()

    def interrupted(self):
        self.end()

    def end(self):
        self.DT.setMode("Direct")
        self.DT.tankDrive(0,0)
