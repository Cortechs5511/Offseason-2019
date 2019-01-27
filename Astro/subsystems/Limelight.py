import math

from wpilib import SmartDashboard
from networktables import NetworkTables

class Limelight():

    abox = 22 #double check if exactly 20

    def __init__(self, Robot):
        self.table = NetworkTables.getTable("limelight")
        self.table.putNumber('ledMode',1)
        self.tv = 0
        self.tx = 0
        self.ty = 0
        self.ta = 0
        self.ts = 0
        self.tl = 0

    def readLimelightData(self):
        self.tv = self.table.getNumber('tv',None)
        self.tx = self.table.getNumber('tx',0)
        self.ty = self.table.getNumber('ty',None)
        self.ta = self.table.getNumber('ta',None)
        self.ts = self.table.getNumber('ts',None)
        self.tl = self.table.getNumber('tl',None)

    def get(self):
        return [self.tv, self.tx, self.ty, self.ta, self.ts, self.tl]

    def getTv(self): return self.tv
    def getTx(self): return self.tx
    def getTy(self): return self.ty
    def getTa(self): return self.ta
    def getTs(self): return self.ts
    def getTl(self): return self.tl

    def getDistance(self):
        const = 4 * math.tan(0.471)*math.tan(0.3576)
        if(self.ta==None or self.ta==0): return -1
        return math.sqrt((self.abox)/(const*self.ta))

    def getHorizontal(self): return self.tx
    def getVertical(self): return self.ty
    def getArea(self): return self.ta
    def getAngle2(self): pass

    def dashboardInit(self):
        pass

    def dashboardPeriodic(self):
        #SmartDashboard.putNumber("Limelight_tv", self.tv)
        SmartDashboard.putNumber("Angle1", self.tx)
        #SmartDashboard.putNumber("Angle2", self.getAngle2())
        #SmartDashboard.putNumber("Limelight_tv", self.ta)
        #SmartDashboard.putNumber("Limelight_tv", self.ts)
        #SmartDashboard.putNumber("Limelight_tv", self.tl)
        #SmartDashboard.putNumber("Limelight_tv", self.tl)
        SmartDashboard.putNumber("Distance",self.getDistance())
