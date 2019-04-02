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
        self.DT.zeroEncoders()
        p = SmartDashboard.getNumber("DriveStraight_P", 0.1)
        i = SmartDashboard.getNumber("DriveStraight_I", 0)
        d = SmartDashboard.getNumber("DriveStraight_D", 0.4)
        angleP = SmartDashboard.getNumber('DriveStraightAngle_P', 0.025)
        angleI = SmartDashboard.getNumber('DriveStraightAngle_I', 0.0)
        angleD = SmartDashboard.getNumber('DriveStraightAngle_D', 0.01)
        self.DT.setGains(p, i, d, 0)
        self.DT.setGainsAngle(angleP, angleI, angleD, 0)
        self.distance = self.distance + self.DT.getAvgDistance()
        self.DT.setCombined(distance=self.distance, angle=self.angle)

    def execute(self):
        self.DT.tankDrive()

    def isFinished(self):
        return (abs(self.distance-self.DT.getAvgDistance())<0.1 and self.DT.getAvgAbsVelocity()<0.2) or self.isTimedOut()

    def interrupted(self):
        self.end()

    def end(self):
        self.DT.setMode("Direct")
        self.DT.tankDrive(0,0)
