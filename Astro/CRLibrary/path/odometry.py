import math

from CRLibrary.util import units

class Odometer():

    def __init__(self, period=1/50, x=0, y=0, angle=0, fudgeX=1, fudgeY=1):
        self.period = period
        self.fudgeX = fudgeX
        self.fudgeY = fudgeY

        [self.x, self.y, self.angle, self.rightVel, self.leftVel] = [x, y, angle, 0, 0]

    def getPeriod(self):
        return self.period

    def update(self, leftV, rightV, angleIn):
        self.leftVx = math.cos(math.pi/180*angleIn) * leftV * self.fudgeX
        self.leftVy = math.sin(math.pi/180*angleIn) * leftV * self.fudgeY
        self.leftVel = (self.leftVx**2 + self.leftVy**2)**0.5

        self.rightVx = math.cos(math.pi/180*angleIn) * rightV * self.fudgeX
        self.rightVy = math.sin(math.pi/180*angleIn) * rightV * self.fudgeY
        self.rightVel = (self.rightVx**2 + self.rightVy**2)**0.5

        speed = ((self.leftVel + self.rightVel))/2
        self.x += speed * self.period * math.cos(math.pi/180*angleIn)
        self.y += speed * self.period * math.sin(math.pi/180*angleIn)

        #Can be updated to assume constant curvature as opposed to constant velocity (see Tyler's book)
        self.angle = angleIn

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

    def reset(self, x=0, y=0, angle=0):
        self.x = x
        self.y = y
        self.angle = angle
        self.rightVel = 0
        self.leftVel = 0
