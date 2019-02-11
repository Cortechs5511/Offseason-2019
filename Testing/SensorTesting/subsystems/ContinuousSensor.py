import wpilib
from wpilib.command import Command
from wpilib.command.subsystem import Subsystem

class ContinuousSensor(Subsystem):

    def __init__(self, function, estimate = 0):
        self.function = function
        self.measurement = 0
        self.estimate = estimate
        self.prediction = 0
        self.g = 0 #g value
        self.h = 0 #h value
        self.time_step = 0
        self.gain = 0

    def update(self):
        self.measurement = self.function()
        self.time_step += 1
        self.prediction = self.estimate + self.gain
        self.gain += (self.h * (self.measurement - self.prediction) / self.time_step)
        self.estimate = self.prediction + (self.g * (self.measurement - self.prediction))

    def returnValue(self):
        return self.estimate
