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
        self.DT.zeroEncoders()
        p = SmartDashboard.getNumber("DriveStraight_P", 0.1)
        i = SmartDashboard.getNumber("DriveStraight_I", 0)
        d = SmartDashboard.getNumber("DriveStraight_D", 0.4)
        angleP = SmartDashboard.getNumber('DriveStraightAngle_P', 0.025)
        angleI = SmartDashboard.getNumber('DriveStraightAngle_I', 0.0)
        angleD = SmartDashboard.getNumber('DriveStraightAngle_D', 0.01)
        self.DT.setGains(p, 0, d, 0)
        self.DT.setGainsAngle(angleP, angleI, angleD, 0)
        StartAngle = self.DT.getAngle()
        self.DT.setMode("Combined", name=None, distance=self.setpoint, angle=StartAngle)

    def execute(self):
        curr = self.DT.getAvgDistance()
        #IZONE
        self.DT.tankDrive()

    def isFinished(self):
        distErr = self.setpoint-self.DT.getAvgDistance()
        SmartDashboard.putNumber("PID DistErr", distErr)
        return (abs(distErr)<0.1 and self.DT.getAvgAbsVelocity()<0.2) or self.isTimedOut()

    def interrupted(self):
        self.end()

    def end(self):
        self.DT.setMode("Direct")
        self.DT.tankDrive(0,0)
