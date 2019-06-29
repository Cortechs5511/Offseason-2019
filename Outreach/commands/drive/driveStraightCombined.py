import math
import wpilib
from wpilib import SmartDashboard
from wpilib.command import Command
from wpilib.command import TimedCommand

class DriveStraightCombined(TimedCommand):

    def __init__(self, distance = 10, angle = 0, timeout = 0, p=1000, i=1000, d=1000):
        super().__init__('DriveStraightCombined', timeoutInSeconds = timeout)

        self.requires(self.getRobot().drive)
        self.DT = self.getRobot().drive

        self.distanceRelative = distance/12
        self.angle = angle
        self.pCheck = p
        self.iCheck = i
        self.dCheck = d

    def initialize(self):
        #self.DT.zeroEncoders()
        # GETTING VALUE FROM DASHBOARD IF P,I,D ARGUMENTS ARE NOT GIVEN WHEN COMMAND IS CALLED
        if self.pCheck == 1000:
            p = SmartDashboard.getNumber("DriveStraight_P", 0.1)
        else:
            p = self.pCheck

        if self.iCheck == 1000:
            i = SmartDashboard.getNumber("DriveStraight_I", 0)
        else:
            i = self.iCheck

        if self.dCheck == 1000:
            d = SmartDashboard.getNumber("DriveStraight_D", 0.4)
        else:
            d = self.dCheck

        angleP = SmartDashboard.getNumber('DriveStraightAngle_P', 0.025)
        angleI = SmartDashboard.getNumber('DriveStraightAngle_I', 0.0)
        angleD = SmartDashboard.getNumber('DriveStraightAngle_D', 0.01)
        self.DT.setGains(p, i, d, 0)
        self.DT.setGainsAngle(angleP, angleI, angleD, 0)
        self.distance = self.distanceRelative + self.DT.getAvgDistance()
        self.DT.setCombined(distance=self.distance, angle=self.angle)

    def execute(self):
        self.DT.tankDrive()

    def isFinished(self):
        return (abs(self.distance-self.DT.getAvgDistance())<0.1 and self.DT.getAvgAbsVelocity()<0.5) or self.isTimedOut()

    def interrupted(self):
        self.end()

    def end(self):
        self.DT.setMode("Direct")
        SmartDashboard.putNumber("Distance Driven", self.DT.getAvgDistance() - self.distance)
        self.DT.tankDrive(0,0)
