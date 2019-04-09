import math

import wpilib
from wpilib import SmartDashboard
from networktables import NetworkTables

class Limelight():

    abox = 92.25 #area of box around targets

    def __init__(self, Robot):
        self.robot = Robot
        self.table = NetworkTables.getTable("limelight")
        self.table.putNumber('ledMode',1)
        self.tv = 0
        self.tx = 0
        self.ty = 0
        self.ta = 0
        self.ts = 0
        self.tl = 0
    def readLimelightData(self):
        self.tv = self.table.getNumber('tv',1000)
        self.tx = self.table.getNumber('tx',1000)
        self.ty = self.table.getNumber('ty',1000)
        self.ta = self.table.getNumber('ta',1000)
        self.ts = self.table.getNumber('ts',1000)
        self.tl = self.table.getNumber('tl',1000)
        self.thor = self.table.getNumber('thor',1000)
        self.tvert = self.table.getNumber('tvert',1000)
        self.tlong = self.table.getNumber('tlong',1000)
        self.tshort = self.table.getNumber('tshort',1000)
        #self.camTran = self.table.getNumberArray('camtran',None)

    def get(self):
        return [self.tv, self.tx, self.ty, self.ta]

    def getAll(self):
        return [self.tv, self.tx, self.ty, self.ta, self.ts, self.tl, self.thor, self.tvert, self.tlong, self.tshort]

    def getTv(self): return self.tv
    def getTx(self): return self.tx
    def getTy(self): return self.ty
    def getTa(self): return self.ta
    def getTs(self): return self.ts
    def getTl(self): return self.tl
    def getThor(self): return self.thor
    def getTvert(self): return self.tvert
    def getTlong(self): return self.tlong
    def getTshort(self): return self.tshort

    def getDistance(self):
        """returns distance in inches from limelight to target"""
        taBox = (self.thor * self.tvert)/(720*960) #box area as percentage of whole
        if(taBox==None or taBox<=0): return -1
        const = 4 * math.tan(0.471)*math.tan(0.3576)
        return math.sqrt((self.abox)/(const*taBox))

    def getAngle2(self):
        #return self.robot.drive.getAngle() - self.getTa() #idk if typo
        return self.robot.drive.getAngle() - self.getTx()

    def getXError(self):
        return self.robot.limelight.getDistance() * math.sin(math.radians(self.getAngle2()))

    def getYError(self):
        return self.robot.limelight.getDistance() * math.cos(math.radians(self.getAngle2()))

    def getPath(self):
        '''returns - amount to drive forward on same angle
        starting angle (maintain while driving forward)
        amount to drive forward while approaching straight on
        '''
        x = self.getXError()
        y = self.getYError()
        angle = self.robot.drive.getAngleAutoAlign()
        dist1 = x/math.cos(math.radians(angle))
        dist2 = y - (dist1 * math.sin(math.radians(angle)))
        return [angle, dist1, dist2]

    def getPathXY(self):
        if wpilib.RobotBase.isSimulation(): return [-10, -5]
        return [-self.getYError()/12, self.getXError()/12]

    def dashboardInit(self):
        pass

    def dashboardPeriodic(self):
        SmartDashboard.putNumber("xError", self.getXError())
        SmartDashboard.putNumber("yError", self.getYError())
        SmartDashboard.putNumber("Distance",self.getDistance())
        SmartDashboard.putNumber("thor", self.thor)
        SmartDashboard.putNumber("Angle1", self.tx)
        SmartDashboard.putNumber("Angle2", self.getAngle2())
        SmartDashboard.putNumber("NavXAngle", self.robot.drive.getAngle())
