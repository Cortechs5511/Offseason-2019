import math
import wpilib

from wpilib.command import Command
from wpilib.command import TimedCommand

from CRLibrary.path import PathFinder
from CRLibrary.path import Ramsetes
from CRLibrary.path import odometry as od

class Align(TimedCommand):

    name = ""

    def __init__(self, follower="PathFinder", timeout = 4):
        super().__init__('Align', timeoutInSeconds = timeout)

        self.requires(self.getRobot().drive)
        self.DT = self.getRobot().drive

        self.follower = follower
        self.Path = self.DT.Path

        self.startX = 0
        self.startY = 0

    def start(self, x=0, y=0):
        [self.startX, self.startY] = [x, y]

        if(y<-2): self.name = "AlignLeft"
        elif(y>2): self.name= "AlignRight"
        else: self.name = "AlignBack"
        #else: self.name = "DriveStraight"
        print(self.name)

        super(Align, self).start()

    def initialize(self):
        self.Path.reset(x = self.startX, y = self.startY, angle = 0)
        self.DT.setPath(name = self.name, follower = self.follower)
        self.distStart = self.DT.getDistance()

    def execute(self):
        self.DT.tankDrive()

    def isFinished(self):
        return self.Path.isFinished() or self.isTimedOut()

    def interrupted(self):
        self.end()

    def end(self):
        self.DT.tankDrive(0,0)
        self.Path.disablePID()
        distEnd = self.DT.getDistance()
        print("DistanceLeft: " , distEnd[0] - self.distStart[0],"DistanceRight: " , distEnd[1] - self.distStart[1])
