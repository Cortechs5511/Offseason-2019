import math
import wpilib
#from robot import MyRobot
#from subsystems.Drive import Drive
import map
from wpilib.command import Command
from wpilib.command import TimedCommand
from wpilib import SmartDashboard
from wpilib.drive.differentialdrive import DifferentialDrive

class SetSpeedDT(TimedCommand):
    def __init__(self, timeout = 0):
        super().__init__('SetSpeedDT', timeoutInSeconds = timeout)
        self.robot = self.getRobot()
        self.requires(self.robot.drive)
        self.DT = self.robot.drive

        self.Joystick0 = self.robot.joystick0 #this is pretty messed up lol
        self.Joystick1 = self.robot.joystick1

    def initialize(self):
        self.DT.setDirect()

    def execute(self):
        left = -self.Joystick0.getY() #also messed up :\
        right = -self.Joystick1.getY()

        if self.robot.readDriverRightButton(map.halfSpeed) or self.robot.readDriverLeftButton(map.halfSpeed):
            [left, right] = [left*.75, right*.75]

        if self.robot.readDriverRightButton(map.flip) or self.robot.readDriverLeftButton(map.flip):
            [left, right] = [-right, -left]

        self.DT.tankDrive((left * 0.85), (right * 0.85))

    def isFinished(self):
        return False

    def interrupted(self): self.end()

    def end(self): self.DT.tankDrive(0,0)
