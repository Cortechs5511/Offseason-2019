import math
import wpilib

from wpilib import SmartDashboard
from wpilib.command import Command
from wpilib.command import TimedCommand

class autonRotation(Command):
    def __init__(self, angle = -135, timeout = 0):
        super().__init__('autonRotation')
        self.requires(self.getRobot().drive)
        self.drive = self.getRobot().drive
        self.angle = angle
        
    def initialize(self):
        self.startAngle = self.drive.getAngle()
        self.drive.setDirect()

    def execute(self):
        leftPower = 0.5 
        rightPower = -0.5
        self.drive.tankDrive(leftPower, rightPower)
        
    def isFinished(self):
        getCurrentAngle = self.drive.getAngle()
        turned = getCurrentAngle-self.startAngle
        error = self.angle - turned
        SmartDashboard.putNumber("turned", turned)
        SmartDashboard.putNumber("turn error", error)
        if abs(error) < 15:
            return True
        else:
            return False
        
    def interrupted(self):
        self.end()

    def end(self):
        self.drive.tankDrive(0,0)

    







