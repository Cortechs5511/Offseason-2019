from wpilib.command import Subsystem
from wpilib.command import Command
import robot
import subsystems
import robotmap

class GetPower(Command):
    def _init__(self, robot):
        self.drive = self.getRobot().drive
        self.requires(self.drive)

    def initialize(self):
        self.leftJs = robotmap.leftJs
        self.rightJs = robotmap.rightJs

    def execute(self):
        maxSpeed = .85
        if abs(self.leftJs.getY()) >= .04:
            self.leftPower = self.leftJs*maxSpeed
        else:
            self.leftPower = 0
        if abs(self.rightJs.getY()) >= .04:
            self.rightPower = self.rightJs*maxSpeed
        else:
            self.rightPower = 0
        self.drive.setPower(self.leftPower,self.rightPower)
