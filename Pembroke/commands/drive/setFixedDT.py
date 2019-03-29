import math
import wpilib

from wpilib.command import Command
from wpilib.command import TimedCommand

class SetFixedDT(TimedCommand):

    def __init__(self, leftSpeed = 0, rightSpeed = 0, timeout = 300):
        super().__init__('SetFixedDT', timeoutInSeconds = timeout)

        self.requires(self.getRobot().drive)
        self.DT = self.getRobot().drive

        self.leftSpeed = leftSpeed
        self.rightSpeed = rightSpeed

    def initialize(self):
        self.DT.setMode("Direct")

    def execute(self):
        self.DT.tankDrive(self.leftSpeed,self.rightSpeed)

    def interrupted(self):
        self.end()

    def end(self):
        self.DT.tankDrive(0,0)
