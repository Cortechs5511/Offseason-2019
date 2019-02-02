#testing endoders
import math
import wpilib

from wpilib.command import Command
from wpilib.command import TimedCommand
from wpilib import SmartDashboard as sd

class Measured(Command):
    '''test command for checking bump detection'''
    def __init__(self):
        self.debug = True
        super().__init__('Measured')
        self.DT = self.getRobot().drive

    def initialize(self):
        self.enc = self.DT.getDistance()

    def execute(self):
        current = self.DT.getDistance()
        sd.putNumber("left distance", current[0]-self.enc[0])
        sd.putNumber("right distance", current[1]-self.enc[1])

    #checking encoders if certain feet acheived
    def isFinished(self):
        return False
