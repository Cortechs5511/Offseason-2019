import math

from CRLibrary.util import units

class Odometer():

    def __init__(self, period):
        self.period = period
        [self.x, self.y, self.angle, self.rightVel, self.leftVel] = [0, 0, 0, 0, 0]

    def getPeriod(self):
        return self.period

    def update(self, leftV, rightV, angleIn):
        speed = (leftV+rightV)/2
        self.x += speed * self.period * math.cos(math.pi/180*angleIn)
        self.y += speed * self.period * math.sin(math.pi/180*angleIn)

        self.angle = angleIn
        self.rightVel = rightV
        self.leftVel = leftV

    def getLeftVelocity(self): return self.leftVel
    def getRightVelocity(self): return self.rightVel
    def getAngle(self): return self.angle

    def get(self): return [self.x, self.y, self.angle, self.leftVel, self.rightVel]

    def getSI(self):
        x = units.feetToMeters(self.x)
        y = units.feetToMeters(self.y)
        angle = units.degreesToRadians(self.angle)
        rightVel = units.feetToMeters(self.rightVel)
        leftVel = units.feetToMeters(self.leftVel)
        return [x, y, angle, leftVel, rightVel]

    def display(self): print(self.get())
