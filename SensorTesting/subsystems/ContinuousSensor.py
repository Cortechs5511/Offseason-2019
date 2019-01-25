import wpilib
from wpilib.command import Command
from wpilib.command.subsystem import Subsystem

class ContinuousSensor(Subsystem):

    def __init__(self, function):
        self.function = function
        self.list = []

    def updateList(self):
        self.value = self.function()
        self.list.append(self.value)

    def returnValue(self, x = 5):
        if len(self.list) >= x:
            self.majorList = []
            for i in range(1,(x+1)):
                self.majorList.append(self.list[-i])
            #self.majorList = [self.list[-1], self.list[-2], self.list[-3], self.list[-4], self.list[-5]]
        elif len(self.list) >= 1:
            self.majorList = [self.list[-1]]
        else:
            return 0
        return (sum(self.majorList) / len(self.majorList))
