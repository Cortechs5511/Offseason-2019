import math

import wpilib
from wpilib import SmartDashboard
from networktables import NetworkTables

class Limelight():

    abox = 92.25 #area of box around targets
    tolAngle = 2

    def __init__(self, Robot):
        self.robot = Robot
        self.table = NetworkTables.getTable("limelight")
        self.table.putNumber('ledMode', 0)
        self.tv = 0
        self.tx = 0
        self.ty = 0
        self.ta = 0
        self.ts = 0
        self.tl = 0
        self.camtran = [0,0,0,0,0,0]

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
        self.camtran = self.table.getNumberArray('camtran', [1000,1000,1000,1000,1000,1000])


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
        if (taBox==None or taBox<=0):
            return -1
        const = 4 * math.tan(0.471)*math.tan(0.3576)
        return math.sqrt((self.abox)/(const*taBox))

    def getAngle2(self):
        #return self.robot.drive.getAngle() - self.getTa() #idk if typo
        return self.robot.drive.getAngle() - self.getTx()

    def getXError(self):
        tx = self.getTx()
        #return self.robot.limelight.getDistance() * math.sin(math.radians(self.getAngle2()))
        angle = self.robot.drive.getAngle()
        angle = abs(angle)
        a = tx + 90 - angle
        de = math.tan(math.radians(a))
        if de == 0:
            return 1000
        else:
            return ((self.getZ()) / (math.tan(math.radians(a)))) + (7.5 * abs(math.sin(math.radians(a))))

    def getYError(self):
        #return self.robot.limelight.getDistance() * math.cos(math.radians(self.getAngle2()))
        tx = self.getTx()
        angle = abs(self.robot.drive.getAngle())
        a = tx + 90 - angle
        return self.getZ() +  (7.5 - 15.2)* abs(math.cos(math.radians(a)))

    def getZ(self):
        return self.camtran[2] * -1

    def getPath(self):
        '''returns - amount to drive forward on same angle
        starting angle (maintain while driving forward)
        amount to drive forward while approaching straight on
        '''
        x = self.getXError()
        y = self.getYError()
        angle0 = 1000
        #x = self.getX3D()
        #y = self.getY3D()
        angle = self.robot.drive.getAngle()
        dist1 = x/abs(math.cos(math.radians(angle)))
        self.dist1 = x/math.cos(math.radians(angle))
        dist2 = y - (dist1 * abs(math.sin(math.radians(angle))))
        self.dist2 = y - (dist1 * math.sin(math.radians(angle)))
        '''if angle is too low it doesnt have time to cover x error'''
        if dist2 < 10:
            angle0 = math.atan(x/(y-10))
            dist2 = 10
            dist1 = (y - 10)/ math.cos(math.radians(angle0))

        dist2 = 1000
        angle0 = 1000
        dist1 = y

        return [angle, dist1 * 2, dist2, angle0]

    def getPathXY(self):
        if wpilib.RobotBase.isSimulation(): return [-10, -5]
        return [-self.getYError()/12, self.getXError()/12]
        #return [-self.getY3D()/12, self.getX3D()/12]

    def dashboardInit(self):
        pass

    def dashboardPeriodic(self):
        SmartDashboard.putNumber("xError", self.getXError())
        SmartDashboard.putNumber("yError", self.getYError())
        SmartDashboard.putNumber('Camtran', self.camtran[2])
        SmartDashboard.putNumber("Distance",self.getDistance())
        SmartDashboard.putNumber("thor", self.thor)
        SmartDashboard.putNumber("Angle1", self.tx)
        SmartDashboard.putNumber("Angle2", self.getAngle2())
        SmartDashboard.putNumber("NavXAngle", self.robot.drive.getAngle())
        SmartDashboard.putNumberArray("Path", self.getPath())
        SmartDashboard.putNumber("dist1", self.dist1)
        SmartDashboard.putNumber("dist2", self.dist2)
