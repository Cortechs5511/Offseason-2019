import math
import wpilib

from wpilib.command import Command
from wpilib.command import TimedCommand
from wpilib import SmartDashboard

class Bump(Command):
    '''test command for checking bump detection'''
    def __init__(self):
        self.debug = True
        super().__init__('Bump')
        self.requires(self.getRobot().drive)
        self.DT = self.getRobot().drive


    def execute(self):
        self.DT.tankDrive(.4, .4)
    def end(self):
        self.DT.disable()
    def interrupted(self):
        self.end()
    def isFinished(self):
        bumpInt = .4
        timeSince = self.timeSinceInitialized()
        timer = 10
        if self.DT.bumpCheck(bumpInt) or timeSince > timer:
        #if abs(self.accelX) >= bumpInt or abstimeSince > timer:
            #print("bump command done")
            return True
        else:
            return False
