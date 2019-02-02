#testing endoders
import math
import wpilib

from wpilib.command import Command
from wpilib.command import TimedCommand
from wpilib import SmartDashboard

class AutonCheck(Command):
    '''test command for checking bump detection'''
    def __init__(self, dist=9.75):
        self.debug = True
        super().__init__('AutonCheck')
        self.requires(self.getRobot().drive)
        self.DT = self.getRobot().drive

        self.dist = dist

    def initialize(self):
        self.start = self.DT.getDistance()
        if self.dist > 0:
            self.mult = 1
        elif self.dist < 0:
            self.mult = -1

    def execute(self):
        distAchieved = abs(self.DT.getDistance()[0]-self.start[0])
        if distAchieved>self.dist:
            distAchieved = distAchieved-self.dist
        else:
            pass
        distToGo = abs(self.dist-distAchieved)
        if distToGo > self.dist:
            distToGo = distToGo - self.dist
        else:
            pass
        #if distAchieved <= .5 * self.dist:
        if distToGo > 5:
            self.DT.tankDrive(.4 * self.mult, .4 * self.mult)
        else:
            speed = min(.4, distToGo/13.2) * self.mult
            self.DT.tankDrive(speed, speed)

    def end(self):
        self.DT.disable()
    def interrupted(self):
        self.end()

    #checking encoders if certain feet acheived
    def isFinished(self):
        timer = 10
        timeSince = self.timeSinceInitialized()
        #returns feet
        distAchieved = abs(self.DT.getDistance()[0]-self.start[0])
        if distAchieved >= self.dist:
            SmartDashboard.putNumber("autonTime", timeSince)
            return True
        else:
            return False
