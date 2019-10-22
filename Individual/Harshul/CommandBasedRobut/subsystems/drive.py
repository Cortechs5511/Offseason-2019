from wpilib.command import Subsystem
from wpilib import Talon
import subsystems
from commands.getPower import GetPower
import robotmap

class Drive(Subsystem):
    def __init__(self):
        self.frontLeft = Talon(robotmap.Talons.frontLeft)
        self.frontRight = Talon(robotmap.Talons.frontRight)
        self.backLeft = Talon(robotmap.Talons.backLeft)
        self.backRight = Talon(robotmap.Talons.backRight)

    def setPower(self, leftPower, rightPower):
        self.frontLeft,self.backLeft = leftPower
        self.frontRight, self.backRight = rightPower

    def initDefaultCommand(self):
        self.setDefaultCommand(GetPower())
