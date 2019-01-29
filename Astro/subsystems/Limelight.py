import math

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

    def get(self):
        return [self.tv, self.tx, self.ty, self.ta, self.ts, self.tl]

    def getTv(self): return self.tv
    def getTx(self): return self.tx
    def getTy(self): return self.ty
    def getTa(self): return self.ta
    def getTs(self): return self.ts
    def getTl(self): return self.tl

    def getDistance(self):
        """returns distance in inches from limelight to target"""
        taBox = (self.thor * self.tvert)/(102400) #box area as percentage of whole
        const = 4 * math.tan(0.471)*math.tan(0.3576)
        if(taBox==None or taBox==0): return -1
        return math.sqrt((self.abox)/(const*taBox))

    def getHorizontal(self): return self.tx
    def getVertical(self): return self.ty
    def getArea(self): return self.ta
    def getAngle2(self): pass

    def dashboardInit(self):
        pass

    def dashboardPeriodic(self):
        #SmartDashboard.putNumber("Limelight_tv", self.tv)
        SmartDashboard.putNumber("Angle1", self.tx)
        SmartDashboard.putNumber("xError", self.robot.drive.getXError())
        SmartDashboard.putNumber("yError", self.robot.drive.getYError())
        SmartDashboard.putNumber("Angle2", self.robot.drive.getAngle2())
        SmartDashboard.putNumber("NavXAngle", self.robot.drive.getAngle())
        #SmartDashboard.putNumber("Limelight_tv", self.ta)
        #SmartDashboard.putNumber("Limelight_tv", self.ts)
        #SmartDashboard.putNumber("Limelight_tv", self.tl)
        #SmartDashboard.putNumber("Limelight_tv", self.tl)
        SmartDashboard.putNumber("Distance",self.getDistance())
