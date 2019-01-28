import wpilib
import math

import pickle
import os.path
import pathfinder as pf

from CRLibrary.path import odometry as od
from CRLibrary.path import PathFinder
from CRLibrary.path import Ramsetes

class Path():

    follower = "PathFinder"

    def __init__(self, DT, model, odometer, getDistances, follower=None):
        self.odometer = odometer
        self.PathFinder = PathFinder.PathFinder(DT, model, odometer, getDistances)
        self.Ramsetes = Ramsetes.Ramsetes(model, odometer)
        if(follower!=None): self.setFollower(follower)

    def reset(self, x=0, y=0, angle=0):
        self.odometer.reset(x, y, angle)
        self.PathFinder.reset()
        self.Ramsetes.reset()

    def setFollower(self, follower):
        self.follower = follower

    def enablePID(self):
        if(self.follower=="PathFinder"): self.PathFinder.enablePID()
        elif(self.follower=="Ramsetes"): self.Ramsetes.enablePID()

    def disablePID(self):
        if(self.follower=="PathFinder"): self.PathFinder.disablePID()
        elif(self.follower=="Ramsetes"): self.Ramsetes.disablePID()

    def initPath(self, name):
        if(self.follower=="PathFinder"): self.PathFinder.initPath(name)
        elif(self.follower=="Ramsetes"): self.Ramsetes.initPath(name)

    def followPath(self):
        if(self.follower=="PathFinder"): return self.PathFinder.followPath()
        elif(self.follower=="Ramsetes"): return self.Ramsetes.followPath()

    def isFinished(self):
        if(self.follower=="PathFinder"): return self.PathFinder.isFinished()
        elif(self.follower=="Ramsetes"): return self.Ramsetes.isFinished()
        return True
