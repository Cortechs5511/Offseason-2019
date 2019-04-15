import math
import wpilib

from wpilib.command import Command
from wpilib import SmartDashboard

class PythonTest(Command):

    def __init__(self):
        super().__init__("PythonTest")
        self.iteration = 1

    def compute(self, n):
        self.sum = 0
        for i in range(n):
            self.sum =  self.sum + math.cos(i) + math.sin(i) + math.sqrt(i)
        return self.sum

    def loop(self, count):
        for i in range(count):
            self.compute(i)
    def execute(self):
        self.loop(self.iteration)

    def interrupted(self):
        self.end()

    def isFinished(self):
        return True

    def end(self):
        self.runTime = self.timeSinceInitialized()
        SmartDashboard.putNumber("runTime", self.runTime)
        SmartDashboard.putNumber("iteration", self.iteration)
        SmartDashboard.putNumber("iterationsPerSec", self.iteration/self.runTime)
        SmartDashboard.putNumber("sum", self.sum)

        if self.runTime < .1:
            self.iteration = int(self.iteration * 2)
        elif self.runTime > .25:
            self.iteration = int(self.iteration * 0.5)
