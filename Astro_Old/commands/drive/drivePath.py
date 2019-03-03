import math
import wpilib

from wpilib.command import Command
from wpilib.command import TimedCommand

from CRLibrary.path import PathFinder
from CRLibrary.path import Ramsetes
from CRLibrary.path import odometry as od

class DrivePath(TimedCommand):

    startX = 0
    startY = 0

    def __init__(self, name="DriveStraight", follower="PathFinder", timeout = 300):
        super().__init__('DrivePath', timeoutInSeconds = timeout)

        self.requires(self.getRobot().drive)
        self.DT = self.getRobot().drive

        self.name = name
        self.follower = follower

        self.Path = self.DT.Path

    def initialize(self):
        #[x,y] = self.limelight.getPathXY()
        [self.startX,self.startY] = [-10, 0]
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
        #print("DistanceLeft: " , distEnd[0] - self.distStart[0],"DistanceRight: " , distEnd[1] - self.distStart[1])
