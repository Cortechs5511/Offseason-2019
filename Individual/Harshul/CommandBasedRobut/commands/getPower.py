from wpilib.command import Subsystem
from wpilib.command import Command
#import robot
#from subsystems.drive import Drive
import robotmap
import oi

class GetPower(Command):
    def _init__(self, robot):
        self.drive = self.getRobot().drive
        self.requires(self.drive)

    def initialize(self):
        self.leftJs = oi.leftJs
        self.rightJs = oi.rightJs

    def execute(self):
        maxSpeed = .85
        left = oi.getLeftJs()
        right = oi.getRightJs()
        if abs(left) >= .04:
            self.leftPower = left*maxSpeed
        else:
            self.leftPower = 0
        if abs(right) >= .04:
            self.rightPower = right*maxSpeed
        else:
            self.rightPower = 0
        self.drive.setPower(self.leftPower,self.rightPower)

        print(self.rightJs)
